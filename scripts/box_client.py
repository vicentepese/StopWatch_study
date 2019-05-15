from __future__ import print_function
from contextlib import contextmanager
from flask import Flask, request
from multiprocessing import Process, Queue
import os
import time
import subprocess
import json
from boxsdk import OAuth2
from boxsdk import Client
import logging
from StringIO import StringIO

# Remove logging from flask app
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

try:
    basestring
except NameError:
    basestring = str


@contextmanager
def with_flask_server(app):
    '''
    A context manager for a flask server that is run as a separate process.

    The context manager returns a multiprocessing queue, which is the way we
    pass the request arguments back from the HTTP handler to our oauth code.
    '''
    def child_main(q):
        app.mp_queue = q
        app.run(port=8080)

    try:
        q = Queue()
        server = Process(target=child_main, args=(q,))
        server.start()

        yield q

    finally:
        server.terminate()
        server.join()


def _config_get():
    config_path = os.path.expanduser('~/.stopwatch-sync/config.json')

    if not os.path.exists(os.path.dirname(config_path)):
        os.makedirs(os.path.dirname(config_path))

    if os.path.exists(config_path):
        # HACK handle errors in JSON format?
        with open(config_path, 'rb') as f:
            return json.load(f)
    else:
        return {}


def _config_set(key, value):
    config = _config_get()

    config[key] = value

    config_path = os.path.expanduser('~/.stopwatch-sync/config.json')
    with open(config_path, 'wb') as f:
        json.dump(config, f)


def _store_tokens(access_token, refresh_token):
    _config_set('box_access_token', access_token)
    _config_set('box_refresh_token', refresh_token)


def box_client():
    config = _config_get()
    if config.get('box_refresh_token') and config.get('box_access_token'):
        oauth = OAuth2(
            client_id=config.get('box_client_ID'),
            client_secret=config.get('box_client_secret'),
            store_tokens=_store_tokens,
            access_token=config.get('box_access_token'),
            refresh_token=config.get('box_refresh_token'),
        )
    else:
        oauth = _oauth_flow()
    return Client(oauth)


def _oauth_flow():
    app = Flask(__name__)

    @app.route('/stopwatch-box')
    def hello_world():
        app.mp_queue.put(dict(
            state=request.args['state'],
            code=request.args['code'],
        ))
        return (
            'You have successfully authenticated with Box for StopWatch Sync. '
            'You can close this window and return to the terminal.')

    oauth = OAuth2(
        client_id=key['clientID'],
        client_secret=key['clientSecret'],
        store_tokens=_store_tokens,
    )

    with with_flask_server(app) as q:
        auth_url, csrf_token = oauth.get_authorization_url('http://localhost:8080/stopwatch-box')
        subprocess.check_call(['open', auth_url])
        print('''
Your browser has been opened to visit:

{}
'''.format(auth_url))

        request_args = q.get()

        # Sleep for a bit to make sure the page renders before the server is killed
        time.sleep(0.1)

    assert request_args['state'] == csrf_token, 'CSRF token did not match. Expected {} but found {}'.format(
        csrf_token, request_args['state'])

    oauth.authenticate(request_args['code'])

    return oauth


class BoxFileNotFound(Exception):
    '''
    Error thrown when a file or directory is not found in Box.
    '''
    pass


class BoxFS(object):
    '''
    A collection of methods to simplify using the Box API as a file system.

    Since each file system access needs to hit the Box API, all methods have
    a from_dir option that permits running the command assuming that command
    paths should be interpreted relative to the supplied Box Folder object.
    This can be used to improve the performance of code and is particularly
    beneficial when accessing deep paths in Box.
    '''
    def __init__(self, client):
        self.client = client

    def _iter_get_all_items(self, container, limit=100):
        '''
        Iterator over all the items in this container. Uses pagination API to ensure all files are retrieved.
        '''
        offset = 0
        while True:
            items = container.get_items(limit=limit, offset=offset)
            # We terminate the loop if this page has no items
            if not items:
                break
            for item in items:
                yield item
            offset += limit

    def _find_item(self, container, name, create_folder_if_missing=False):
        '''
        Looks for an item in a directory with a matching name. Can optionally create folder if the item is missing.
        '''
        for item in self._iter_get_all_items(container):
            if item['name'] == name:
                return item
        if create_folder_if_missing:
            return container.create_subfolder(name)
        else:
            raise BoxFileNotFound('Could not find folder {} in {}'.format(name, container))

    def _find_path(self, path, from_dir=None, create_folder_if_missing=False):
        if not from_dir:
            # If no directory to start from is supplied, we start from the root directory.
            from_dir = self.client.folder(folder_id='0').get()

        item = from_dir
        for segment in path.split(os.path.sep):
            # HACK we skip empty segments, either because of leading/trailing slash or double slash.
            if not segment:
                continue
            item = self._find_item(item, segment, create_folder_if_missing=create_folder_if_missing)
        return item

    def find_if_exists(self, path, from_dir=None):
        '''
        Returns the file or folder at the path. If it does not exist, this returns None.
        '''
        try:
            return self._find_path(path, from_dir=from_dir)
        except BoxFileNotFound:
            return None

    def makedirs(self, path, from_dir=None):
        '''
        Recursive directory creation function. Does not throw error if leaf folder already exists.
        '''
        return self._find_path(path, create_folder_if_missing=True, from_dir=from_dir)

    def exists(self, path, from_dir=None):
        '''
        Returns whether the file or directory at this path exists.
        '''
        try:
            self._find_path(path, from_dir=from_dir)
            return True
        except BoxFileNotFound:
            return False

    def read(self, path_or_file, from_dir=None):
        '''
        Return the file contents at a given path or for a supplied box file object.
        '''
        if isinstance(path_or_file, basestring):
            f = self._find_path(path_or_file, from_dir=from_dir)
        else:
            f = path_or_file
        s = StringIO()
        f.download_to(s)
        return s.getvalue()

    def write(self, path, data, from_dir=None, force_create=False):
        '''
        Write a file's content to a path. Requires the directory to exist.
        Returns the file object that was written to.

        When force_create is set, this method will always create a new file without checking to see
        if one exists. This option exists primarily to be more performant.
        '''
        folder = self._find_path(os.path.dirname(path), from_dir=from_dir)
        basename = os.path.basename(path)
        s = StringIO(data)
        # In some cases, we prefer to force file creation, as we may be certain the file does not exist.
        if force_create:
            return folder.upload_stream(s, basename)
        try:
            # If the file exists, we simply update the contents.
            existing = self._find_item(folder, basename)
            existing.update_contents_with_stream(s)
            return existing
        except BoxFileNotFound:
            # If the file does not exist, we create the file.
            return folder.upload_stream(s, basename)


if __name__ == '__main__':
    config = _config_get()
    print('current config', config)
    client = box_client()
    me = client.user(user_id='me').get()
    print('user_login: ' + me['login'])
