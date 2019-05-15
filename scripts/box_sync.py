from __future__ import print_function
import utils
from StringIO import StringIO
import pandas as pd
import box_client
import mhealth_client
import os
import data_pb2
import pytz
from datetime import datetime
import hashlib
import math
import numpy as np
import traceback
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import google.protobuf
import zlib
import json
import subprocess


script_dir = os.path.dirname(os.path.abspath(__file__))

tz = pytz.timezone('America/Los_Angeles')


def send_slack(webhook, message):
    if not webhook:
        return
    data = json.dumps(dict(text=message))
    retcode = subprocess.call([
        'curl', '-X', 'POST', '-H', 'Content-type: application/json',
        '--data', data,
        webhook,
    ])
    if retcode != 0:
        print('WARNING: retcode for slack message was nonzero: {}'.format(retcode))


def _is_valid_value(v):
    '''
    This function returns true when the value is something valid for use,
    like a finite number or a string. It returns false for values like
    None, NaN, and empty string. We use this because columns in CSVs are often interpreted by pandas
    as mixed types, so there may be NaNs alongside strings. Because np.isnan throws
    errors when run on strings, we do type checking here to run np.isnan on floats.
    >>> _is_valid_value(3)
    True
    >>> _is_valid_value(3.25)
    True
    >>> _is_valid_value('ID123')
    True
    >>> _is_valid_value(float('nan'))
    False
    >>> _is_valid_value(None)
    False
    >>> _is_valid_value('')
    False
    '''
    try:
        float(v)
        return not np.isnan(v)
    except (ValueError, TypeError):
        # Not a float, so we can rely on truthyness
        return bool(v)


def _utcseconds_to_california(ts):
    return datetime.utcfromtimestamp(ts).replace(tzinfo=pytz.utc).astimezone(tz)


def log(msg):
    print(datetime.now().isoformat(), msg)


pb_type_to_name = {
    data_pb2.AccelerometerSamplesV1: 'accelv1',
    data_pb2.AccelerometerSamplesV2: 'accelv2',
    data_pb2.ActivitySamples: 'activity',
    data_pb2.DeviceMotion: 'devicemotion',
    data_pb2.FocusSession: 'fs',
    data_pb2.PhoneFocusSession: 'phonefs',
}


def _upload_mhealth_file(f, boxfs, mh, participant_record, box_datadir):
    boxfile = None  # setting this so we can check it in rollback
    file_content = None
    try:
        mhealth_id = f['participantId']

        # We download the file from mhealth into memory
        file_content = mh.download_file(f['fileUploadUrl'])

        # Interpret the data as a protobuf, picking out fields we need to construct path below.
        try:
            data = utils._load_data(fileobj=StringIO(file_content))
        except zlib.error as err:
            log('HACK zlib error while loading sequence={}: {}'.format(f['sequence'], str(err)))
            return
        except IOError as err:
            if str(err).startswith('CRC check failed'):
                log('HACK CRC error while loading sequence={}: {}'.format(f['sequence'], str(err)))
                return
            else:
                raise
        data_type = type(data)
        data_start_date = data.date[0] if data_type is data_pb2.DeviceMotion else data.start_date
        if data_type is data_pb2.DeviceMotion:
            log('HACK skipping device motion for sequence={}'.format(f['sequence']))
            return
        data_date = _utcseconds_to_california(data_start_date)
        data_study_id = _clean_participant_id(data.participant_id)

        # HACK Prior versions of the app would upload activity files with only 0 or 1 activity samples.
        # In general, it isn't possible to meaningfully interpret them. We look for these files by
        # filtering for those that are activity, very small in byte count, and have 0 or 1 dates.
        if data_type is data_pb2.ActivitySamples and len(file_content) < 60 and len(data.date) <= 1:
            log('HACK Skipping empty activity file sequence={}'.format(f['sequence']))
            return

        # If this is a new subject, we use this data's ID, otherwise we use the existing ID.
        mh_idx = participant_record.mhealth_id == mhealth_id
        mh_idx_count = mh_idx.sum()

        assert mh_idx_count <= 1, 'Expected one match in participant record for {} but found {}'.format(
            mhealth_id, mh_idx_count)
        study_id_matches_other_rows = (
            ~mh_idx & (participant_record.study_id == data_study_id)).sum()
        assert not study_id_matches_other_rows, 'Found {} other rows with study_id={} when processing {}'.format(
            data_study_id, mhealth_id)

        new_subject = mh_idx_count == 0
        if new_subject:
            assert data_start_date != 0, 'First date for new subject={} seq={} was epoch. Not valid date.'.format(
                mhealth_id, f['sequence'])
            study_id = data_study_id
            study_start = data_date
        else:
            row = participant_record.loc[np.where(mh_idx)[0][0]]
            study_id = row.study_id
            study_start = _utcseconds_to_california(row.study_start_date)

        # HACK if the row's study ID is missing, we name their folder after their mhealth ID.
        if _is_valid_value(study_id):
            participant_folder = study_id
        else:
            participant_folder = 'mhealth_{}'.format(mhealth_id)
            # HACK if we are using the mhealth ID, we might eventually get a proper study ID. warn if so
            if _is_valid_value(data_study_id):
                log('Warning: Rename subject and folder {} to {}'.format(participant_folder, data_study_id))

        # We construct a path that looks like $box_dir/data/SWB4132/week1/2018-01-18-sunday/19:00:00-accelv2.data

        week_number = _study_week_number_for_date(study_start, data_date)
        '''
        HACK HACK HACK deleting this for now as it's the common cause of sync halting.
        assert week_number >= 1,\
            'Expected positive week number, but found {}. Study started {}, but data start is {} {}'.format(
                week_number, study_start.isoformat(), data_date.isoformat(), data_start_date)
        '''
        week_folder = 'week{}'.format(week_number)
        day_folder = data_date.strftime('%Y-%m-%d-%A').lower()
        # Looks like SWB4132/week1/2018-01-18-sunday
        # HACK to make this faster, we assume this is relative to the dir $box_dir/data
        filedir = os.path.join(participant_folder, week_folder, day_folder)

        # This looks like 19:00:00-accelv2.data
        basename = '{}-{}.data'.format(data_date.strftime('%H:%M:%S'), pb_type_to_name[data_type])
        # looks like: SWB4132/week1/2018-01-18-sunday/19:00:00-accelv2.data
        filepath = os.path.join(filedir, basename)

        box_filedir = boxfs.makedirs(filedir, from_dir=box_datadir)

        # If a file exists at this location, we should check to see that they're the same file.
        if boxfs.exists(basename, from_dir=box_filedir):
            existing = boxfs.find_if_exists(basename, from_dir=box_filedir)
            new_sha1 = hashlib.sha1(file_content).hexdigest()

            # If files match, then we don't mind tossing this info out.
            files_match = new_sha1 == existing.sha1
            if files_match:
                log('File already exists for sequence={} at {}'.format(f['sequence'], filepath))
                return

            # The files might have a different participant ID. We next check for that.
            existing_content = None
            try:
                existing_content = boxfs.read(existing)
            except Exception as err:
                print('Error downloading existing content', str(err))
            if existing_content and _protobufs_contain_same_data(
                    data, utils._load_data(fileobj=StringIO(existing_content))):
                log('File with different participant_id already exists for sequence={} at {}'.format(
                    f['sequence'], filepath))
                return

            # HACK to let us skip throwing an error in some cases.
            throw_error = True

            # Focus sessions are saved in a preliminary format to avoid data loss if the FS isn't
            # completed. Unfortunately this incomplete file is sometimes uploaded. We pick the larger
            # file of the two, as this means it has the data we want. This will often be the later file
            # so we will often have to delete the Box file.
            if data_type is data_pb2.FocusSession:
                delete_box = len(existing_content) < len(file_content)
                log('Found duplicate FS file. Box size {}, MH size {}, so {}'.format(
                    len(existing_content), len(file_content), 'deleting box file' if delete_box else 'skipping MH'
                ))
                if delete_box:
                    existing.delete()
                    throw_error = False
                else:
                    return

            if throw_error:
                # We write the collision to disk to make the files easier to analyze.
                simple_f = filepath.replace(os.path.sep, '-')
                if existing_content:
                    with open('collision-box-{}'.format(simple_f), 'wb') as outfile:
                        outfile.write(existing_content)
                with open('collision-new-{}'.format(simple_f), 'wb') as outfile:
                    outfile.write(file_content)

                # When files do not match, we throw an error.
                existing_md = None
                try:
                    existing_md = existing.metadata().get()
                except Exception:
                    pass
                msg = 'Name collision at path {}.\n'.format(filepath)
                msg += 'Existing file sha1: {}, metadata: {}\n'.format(existing.sha1, existing_md)
                msg += 'New file sha1: {}, mhealth: {}'.format(new_sha1, f)
                raise Exception(msg)

        # We write the file to Box.
        boxfile = boxfs.write(basename, file_content, from_dir=box_filedir, force_create=True)
        # We add info from mhealth, as well as all info we extract from the file to metadata to simplify analyses.
        # NOTE need to make sure these values are all strings, otherwise we get errors here.
        boxfile.metadata().create({
            'mh_sequence': str(f['sequence']),
            'mh_uploaded': f['uploaded'],
            'mh_participantId': str(mhealth_id),
            'start_date': data_date.isoformat(),
            'study_id': data_study_id if _is_valid_value(data_study_id) else '__missing__',
        })

        log('Uploaded p{}-s{} to {}'.format(mhealth_id, f['sequence'], filepath))

        return new_subject, mhealth_id, study_id, data_start_date
    except Exception as err:
        if file_content:
            with open('error-file-p{}-s{}'.format(mhealth_id, f['sequence']), 'wb') as f:
                f.write(file_content)
        '''
        if boxfile:
            log('Partial upload occurred. Removing file {}'.format(filepath))
            boxfile.delete()
        '''
        raise


def _wait_for_future(future):
    '''
    This function waits for this future to complete while ensuring things like KeyboardInterrupt can be caught.
    We avoid processing exceptions, instead letting callers choose when to process errors.
    '''
    while True:
        try:
            future.result(timeout=0.1)
            # If we do not timeout, we are done!
            return
        except TimeoutError:
            # timed out... wait again.
            pass
        except Exception:
            # If we have an error, we are done!
            return


def main(box_dir, executor, slack_webhook=None):
    # Login to Box & mHealth
    box = box_client.box_client()
    boxfs = box_client.BoxFS(box)
    mh = mhealth_client.mHealthClient(
        host='https://mhealth-data-qa.stanford.edu/data-KnRJe654r9xkA5tX',
        portal_url='https://mhealth-access-qa.stanford.edu/researcher/',
        credentials_obj=box_client._config_get().get('mhealth_creds'),
        store_credentials=lambda creds: box_client._config_set('mhealth_creds', creds),
    )
    mh.auth_flow()

    # Load list of invalid URLs to skip
    invalid_urls_csv = pd.read_csv(os.path.join(script_dir, 'invalid_urls.csv'))
    invalid_urls = frozenset(invalid_urls_csv.url.values)

    # We store config in a hidden dir.
    config_path = os.path.join(box_dir, '.config')
    box_configdir = boxfs.find_if_exists(config_path)
    if box_configdir:
        sequence_record = pd.read_csv(StringIO(boxfs.read('sequence', from_dir=box_configdir)))
        participant_record = pd.read_csv(StringIO(boxfs.read('participant', from_dir=box_configdir)))
    else:
        # If we have no config dir, we assume the data dir also needs to be set up
        box_configdir = boxfs.makedirs(config_path)
        boxfs.makedirs(os.path.join(box_dir, 'data'))
        # and here is empty state for sync metadata.
        sequence_record = pd.DataFrame([dict(last_sequence=None)])
        participant_record = pd.DataFrame(columns=['mhealth_id', 'study_id', 'study_start_date'])

    log('Starting StopWatch Box sync. Last sequence {}'.format(
        sequence_record.last_sequence.values[0]))

    box_datadir = boxfs.find_if_exists(os.path.join(box_dir, 'data'))

    def _concurrent_file_iter():
        '''
        This function helps simply support concurrent execution of our file iteration. Our below file iteration can
        avoid needing to break out of two loops by letting this function handle the two loops.

        Our concurrency strategy here involves running the mhealth upload for each file in parallel, then yielding the
        futures in in sequence order, so the loop below can check their results and see if they failed or succeeded.
        HACK we should consider running files out of order so that we can avoid conflicts like double uploads &
        duplicate names
        '''
        futures = None
        try:
            for file_page in mh.files_iter(since=sequence_record.last_sequence.values[0], yield_pages=True):
                futures = [
                    (
                        f,
                        executor.submit(_upload_mhealth_file, f, boxfs, mh, participant_record, box_datadir),
                    )
                    for f in file_page
                ]
                # We want to make sure we process them in sequence order, so we process them
                # in the order returned by mhealth.
                for (f, future) in futures:
                    _wait_for_future(future)
                    yield (f, future)
        except (KeyboardInterrupt, Exception, GeneratorExit) as err:
            executor.shutdown(wait=False)
            if futures:
                for (f, future) in futures:
                    # This is a no-op for completed or running futures.
                    future.cancel()
            raise

    counter = 0
    err = None
    try:
        for f, future in _concurrent_file_iter():
            try:
                # Add this sanity check here to make sure we never run data out of order.
                prev = sequence_record.last_sequence.values[0]
                if _is_valid_value(prev):
                    assert prev < f['sequence'], \
                        'Every sequence number must be larger than prior ones. Found {} after {}'.format(
                            f['sequence'], prev)

                if f['fileUploadUrl'] in invalid_urls:
                    log('Skipping invalid URL {}'.format(f['fileUploadUrl']))
                    continue

                result = future.result()
                # Result is None in cases like duplicate files & empty activity.
                if not result:
                    continue
                new_subject, mhealth_id, study_id, data_start_date = result

                # Since the upload has succeeded, we can update the record with a new subject and
                # and note the sequence number.
                if new_subject:
                    participant_record.loc[len(participant_record)] = dict(
                        mhealth_id=mhealth_id,
                        study_id=study_id,
                        study_start_date=data_start_date,
                    )
                sequence_record.last_sequence = f['sequence']

                counter += 1
            except Exception as err:
                print('Error with file', f, str(err))
                try:
                    setattr(err, 'file_info', f)
                except Exception:
                    pass
                traceback.print_exc()
                break
    except KeyboardInterrupt:
        log('Received KeyboardInterrupt - shutting down...')

    # Even if we threw an error above, we didn't update these records unless the loop succeeded,
    # so we can always safely push updates to the sequence & participant.
    boxfs.write('sequence', sequence_record.to_csv(index=False), from_dir=box_configdir)
    boxfs.write('participant', participant_record.to_csv(index=False), from_dir=box_configdir)

    log('Synced {} files to Box'.format(counter))
    msg = 'Synced {} files to Box.'.format(counter)
    if err:
        msg += ' Error: {}.'.format(str(err))
    if hasattr(err, 'file_info'):
        file_info = getattr(err, 'file_info')
        msg += str(file_info)
    send_slack(slack_webhook, msg)


def _study_week_number_for_date(study_start, date):
    '''
    This function computes the week a date occurred relative to the start date of a study.
    We make sure to compare relative to midnight of the day the study started, so that the 7th day is part of the
    2nd week.

    >>> from datetime import datetime, timedelta
    >>> now = datetime(2018, 1, 15, 12, 0)
    >>> _study_week_number_for_date(now, now + timedelta(days=3))
    1
    >>> _study_week_number_for_date(now, now + timedelta(days=6.9))
    2
    >>> _study_week_number_for_date(now, now + timedelta(days=7))
    2
    >>> _study_week_number_for_date(now, now + timedelta(days=16))
    3
    '''
    study_start_midnight = study_start.replace(hour=0, minute=0, second=0, microsecond=0)
    diff = date - study_start_midnight
    seconds_in_week = 60 * 60 * 24 * 7
    return 1 + int(math.floor(diff.total_seconds() / seconds_in_week))


def _protobufs_contain_same_data(a, b):
    '''
    This function compares two protobufs by matching their data fields. In particular,
    this means that they won't compare the participant_id fields, which can differ
    if a protobuf was exported twice from a device.

    >>> a = data_pb2.AccelerometerSamplesV2(participant_id='a', x=[1, 2, 3])
    >>> other_type = data_pb2.DeviceMotion()
    >>> _protobufs_contain_same_data(a, None)
    False
    >>> _protobufs_contain_same_data(None, a)
    False
    >>> _protobufs_contain_same_data({}, a)
    False
    >>> _protobufs_contain_same_data(a, {})
    False
    >>> _protobufs_contain_same_data(a, other_type)
    False
    >>> b = data_pb2.AccelerometerSamplesV2(participant_id='a', x=[1, 2])
    >>> _protobufs_contain_same_data(a, b), a == b
    (False, False)
    >>> b.x.append(3)
    >>> _protobufs_contain_same_data(a, b), a == b
    (True, True)
    >>> b.participant_id = 'b'
    >>> _protobufs_contain_same_data(a, b), a == b
    (True, False)
    '''
    # We want to ensure the arguments are both protobuf messages of the
    # appropriate type before proceeding.
    if (
        a is None or
        b is None or
        not isinstance(a, google.protobuf.message.Message) or
        not isinstance(b, google.protobuf.message.Message) or
        a.DESCRIPTOR is not b.DESCRIPTOR
    ):
        return False

    for k in a.DESCRIPTOR.fields_by_name.keys():
        # We skip participant_id as this can be incorrect or unset in some cases.
        if k == 'participant_id':
            continue
        if getattr(a, k) != getattr(b, k):
            return False
    return True


def _clean_participant_id(participant_id):
    '''
    This function cleans up a participant ID, ensuring that we only detect a valid participant ID. In particular,
    this ignores empty string, None and "???", which are all invalid IDs and are set as default values in some cases.
    >>> _clean_participant_id('???')
    >>> _clean_participant_id('')
    >>> _clean_participant_id(None)
    >>> _clean_participant_id('ID123')
    'ID123'
    '''

    # HACK "???" is the participant ID we include when it was not passed from the phone to the watch.
    if participant_id and participant_id != '???':
        return participant_id
    # This might be an empty string or None, depending on the way this was serialized and other factors.
    else:
        return None


if __name__ == '__main__':
    import argparse

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('box_dir', help='The path to the data directory in box', type=str)
    arg_parser.add_argument('--test', help='Run some tests.', action='store_true')
    arg_parser.add_argument('--slack_webhook', help='The webhook to slack', type=str)
    args = arg_parser.parse_args()

    if args.test:
        import doctest
        result = doctest.testmod()
        FAIL = '\033[91m'
        OKGREEN = '\033[92m'
        ENDC = '\033[0m'
        if result.failed:
            print(FAIL + '{} of {} failed'.format(result.failed, result.attempted) + ENDC)
        else:
            print(OKGREEN + 'All tests passed!' + ENDC)
    else:
        with ThreadPoolExecutor(max_workers=1) as executor:
            main(args.box_dir, executor, slack_webhook=args.slack_webhook)
