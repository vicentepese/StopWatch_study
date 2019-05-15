from datetime import datetime
import pytz
import gzip
from scripts import data_pb2


def _load_data(filename=None, fileobj=None):
    assert filename or fileobj, 'Must supply either filename or fileobj.'
    with gzip.GzipFile(filename=filename, fileobj=fileobj, mode='rb') as f:
        data = f.read()

    samples = None
    err = None

    if not samples:
        try:
            samples = data_pb2.AccelerometerSamplesV2()
            samples.ParseFromString(data)
            assert len(samples.z) == len(samples.date), 'len of date and z do not match'
            assert len(samples.z), 'must have some number of samples'
        except Exception as err:
            samples = None

    if not samples:
        try:
            samples = data_pb2.FocusSession()
            samples.ParseFromString(data)
            dm = samples.device_motion
            assert len(dm.gravity.z), 'must have some number of samples'
            assert len(dm.date), 'must have some number of samples'
            # HACK we have to do something complicated here b/c of an issue with
            # sequence 25279. We are taking the larger of the two sets of samples.
            # We throw an error if one of the sets of samples is missing 1% or more
            # samples relative to the larger of the two sets. This will help us
            # process data that has some strange issues where data storage/serialization
            # must have been halted in some way.
            if len(dm.gravity.z) != len(dm.date):
                print(
                    'Warning: found sample count discrepancy in focus session data. '
                    'len(gravity.z)={} len(date)={}'.format(len(dm.gravity.z), len(dm.date))
                )
            max_len = max(len(dm.gravity.z), len(dm.date))
            assert max_len * 0.95 < len(dm.gravity.z), 'Much smaller number of gravity samples'
            assert max_len * 0.95 < len(dm.date), 'Much smaller number of date samples'
        except Exception as err:
            samples = None

    if not samples:
        try:
            samples = data_pb2.PhoneFocusSession()
            samples.ParseFromString(data)
            dm = samples.device_motion
            assert len(dm.gravity.z) == len(dm.date), 'len of date and z do not match'
            assert len(dm.gravity.z), 'must have some number of samples'
        except Exception as err:
            samples = None

    if not samples:
        try:
            samples = data_pb2.DeviceMotion()
            samples.ParseFromString(data)
            dm = samples
            assert len(dm.gravity.z) == len(dm.date), 'len of date and z do not match'
            assert len(dm.gravity.z), 'must have some number of samples'
        except Exception as err:
            samples = None

    if not samples:
        try:
            samples = data_pb2.AccelerometerSamplesV1()
            samples.ParseFromString(data)
            assert len(samples.z) == len(samples.date), 'len of date and z do not match'
            assert len(samples.z), 'must have some number of samples'
        except Exception as err:
            samples = None

    if not samples:
        try:
            samples = data_pb2.ActivitySamples()
            samples.ParseFromString(data)
            assert len(samples.stationary) == len(samples.date), 'len of date and stationary do not match'
            # HACK we don't force this requirement as we have no samples in some cases.
            # so we must ensure this runs at the very end to avoid this kind of issue.
            # assert len(samples.stationary), 'must have some number of samples'
        except Exception as err:
            samples = None

    if not samples:
        raise err

    return samples


tz = pytz.timezone('America/Los_Angeles')


def _parse_date(ts):
    return datetime.utcfromtimestamp(ts).replace(tzinfo=pytz.utc).astimezone(tz)
