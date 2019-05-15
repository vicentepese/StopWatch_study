from __future__ import print_function
import requests
import getpass
import time
import StringIO
import subprocess
import numpy as np
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def requests_retry_session(
    retries=10,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    '''
    Creates a requests session that will retry when the server has errors.
    We're willing to wait relatively long periods of time to give the server a
    chance to reply.
    Copied from https://www.peterbe.com/plog/best-practice-with-retries-with-requests
    '''
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


class StanfordNetworkAccessDeniedException(Exception):
    '''
    Error thrown when accessing mHealth via an insecure network connection.
    '''
    pass


class mHealthClient(object):
    '''
    Default settings:
    mHealthClient(
        host='https://mhealth-data-qa.stanford.edu/data-KnRJe654r9xkA5tX',
        portal_url='https://mhealth-access-qa.stanford.edu/researcher/',
    )
    '''
    def __init__(self, host, portal_url=None, credentials_obj=None, store_credentials=None):
        self.host = host
        self.portal_url = portal_url
        self.credentials_obj = credentials_obj
        self.store_credentials_callback = store_credentials
        self.download_session = requests_retry_session()

    def auth_flow(self):
        '''
        Starts the authentication flow. If the credentials aren't expired, this is a noop. If the credentials are
        expired or unset, this will open the portal and request a refresh token.
        '''
        creds = self.credentials_obj

        expired = creds and time.time() > creds['expire_time']

        if expired or not creds:
            if creds:
                token = creds['refresh_token']
            else:
                if self.portal_url:
                    subprocess.check_call(['open', self.portal_url])
                    print('''
Your browser has been opened to visit:

{}
'''.format(self.portal_url))
                token = getpass.getpass('Refresh Token: ')
            creds = self._refresh(token)
            creds['expire_time'] = creds['expires_in'] + time.time()

            self.credentials_obj = creds
            if self.store_credentials_callback:
                self.store_credentials_callback(creds)

    def _refresh(self, token):
        r = requests.post(
            self.host + '/api/v1/token',
            data=dict(grant_type='refresh_token', refresh_token=token))
        r.raise_for_status()
        return r.json()

    def api_request(self, url, method='GET', params=None, session=None):
        '''
        A method that can make authenticated requests to the API.
        '''
        assert self.credentials_obj, 'Need to be authenticated to make request to API'
        if url[0] == '/':
            url = self.host + url
        else:
            assert url.startswith(self.host), 'URL for request {} did not start with host {}'.format(url, self.host)
        params = params or {}
        r = (session or requests).request(
            method,
            url,
            params=params,
            headers={'Authorization': 'Bearer {}'.format(self.credentials_obj['access_token'])})
        if 'Network Access Denied' in r.text:
            raise StanfordNetworkAccessDeniedException()
        r.raise_for_status()
        return r

    def files(self, since=None, order=None, pg=None):
        '''
        Request a list of files. Refer to mHealth docs for more details.
        '''
        p = {}
        if since is not None and not np.isnan(since):
            p['since'] = since
        if order is not None:
            p['order'] = order
        if pg is not None and not np.isnan(pg):
            p['pg'] = pg
        return self.api_request(self.host + '/api/v1/files', params=p).json()

    def download_file(self, url, origfileobj=None):
        r = self.api_request(url, session=self.download_session)
        fileobj = origfileobj or StringIO.StringIO()
        for chunk in r.iter_content(4096):
            fileobj.write(chunk)

        # When no fileobj is passed in, we return the string value of the file.
        if not origfileobj:
            return fileobj.getvalue()

    def files_iter(self, since=None, yield_pages=False):
        '''
        This is used to iterate over all files following the supplied sequence number `since`. We force
        the file iteration order to be ascending, so any modifications to state based on this will result
        in consistent computations.

        Although the mHealth API permits pagination via the pg parameter, it seems to have occasional
        bugs where a page is repeated when requesting the consecutive page. This method instead always
        requests pg=1, but changes the `since` parameter to be the largest value from the prior page.

        The yield_pages parameter yields an entire page of files at a time, as opposed to a single file at
        a time when false.
        '''
        while True:
            files = self.files(pg=1, order='asc', since=since)
            if yield_pages:
                yield files['dataUrls']
            else:
                for dataUrl in files['dataUrls']:
                    yield dataUrl
            if files['nextPage']:
                since = max(f['sequence'] for f in files['dataUrls'])
            else:
                break


if __name__ == '__main__':
    client = mHealthClient(
        host='https://mhealth-data-qa.stanford.edu/data-KnRJe654r9xkA5tX',
        portal_url='https://mhealth-access-qa.stanford.edu/researcher/',
    )
    client.auth_flow()

    print('page 1 asc')
    files = client.files(pg=1, order='asc')
    print('response', dict(files, dataUrls=[f['sequence'] for f in files['dataUrls']]))

    print('page 1 asc since=487')
    files = client.files(pg=1, order='asc', since=487)
    print('response', dict(files, dataUrls=[f['sequence'] for f in files['dataUrls']]))

    print('page 1 desc')
    files = client.files(pg=1, order='desc')
    print('response', dict(files, dataUrls=[f['sequence'] for f in files['dataUrls']]))

    print('page 1 desc since=19021')
    files = client.files(pg=1, order='desc', since=19021)
    print('response', dict(files, dataUrls=[f['sequence'] for f in files['dataUrls']]))

    print('page 1 asc since=19021')
    files = client.files(pg=1, order='asc', since=19021)
    print('response', dict(files, dataUrls=[f['sequence'] for f in files['dataUrls']]))
