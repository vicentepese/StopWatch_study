import os
from glob import glob
import matplotlib.pyplot as plt
import numpy as np
import msgpack
import gzip
import pandas as pd
from collections import OrderedDict
from scripts import data_pb2
from tqdm import tqdm_notebook as tqdm
from datetime import datetime
import pytz
import scripts.utils as sw_util
import matplotlib
from scripts.utils import _load_data as load_data


class DataManager:

    def __init__(self, save_path, base_dir):
        if base_dir[-1] is not '/':
            self.base_dir = base_dir + '/'
        else:
            self.base_dir = base_dir
        if save_path[-1] is not '/':
            self.save_path = save_path + '/'
        else:
            self.save_path = save_path
        self.save_path_phone = os.path.join(self.save_path, 'Phone')
        self.save_path_watch = os.path.join(self.save_path, 'Watch')

    def get_base_dir(self, prt=False):
        if prt:
            print(self.base_dir)
        return self.base_dir

    def get_save_dir(self, prt=False):
        if prt:
            print(self.save_path)
        return self.save_path

    def get_subjects(self, prt=False):
        if prt:
            print(os.listdir(self.base_dir))
        return os.listdir(self.base_dir)

    def get_patients(self, prt=False):

        # Take patients
        subjects = self.get_subjects()
        patients = [patient for patient in subjects if patient.isdigit()]
        mhealth = [patient for patient in subjects if '_' in patient]

        # Remove mhealth to homogenize
        rm_ = lambda p: (p[p.find('_') + 1:])
        patients = patients + [patient for patient in map(rm_, mhealth)]

        if prt:
            print(patients)

        return patients

    def get_controls(self, prt=False):

        # Take controls
        subjects = self.get_subjects()
        controls = [control for control in subjects if not control.isdigit()]

        return controls

    def get_weeks(self, patient_id, prt=False):
        if prt:
            print(os.listdir(glob(os.path.join(self.base_dir, patient_id))[-1]))
        return os.listdir(glob(os.path.join(self.base_dir, patient_id))[-1])

    def get_recording_sessions(self, patient_id, week, prt=False):
        recordings_session_path = self.get_recording_sessions_path(patient_id=patient_id, week=week)
        if prt:
            print(os.listdir(recordings_session_path))
        return os.listdir(recordings_session_path)

    def get_recording_data(self, patient_id, week, recording_session, prt=False):
        recordings_path = self.get_recording_path(patient_id=patient_id, week=week, recording_session=recording_session)
        if prt:
            print(os.listdir(recordings_path))
        return os.listdir(recordings_path)

    def get_recording_sessions_path(self, patient_id, week):
        return glob(os.path.join(self.base_dir, patient_id + '/' + week + '/'))[-1]

    def get_recording_path(self, patient_id, week, recording_session):
        recording_session_path = self.get_recording_sessions_path(patient_id=patient_id, week=week)

        return glob(os.path.join(recording_session_path, recording_session + '/'))[-1]

    def read_data(self, patient_id, week, recording):
        recording_session_path = self.get_recording_sessions_path(patient_id=patient_id, week=week)
        path_to_file = glob(os.path.join(recording_session_path + recording))[-1]

        return load_data(path_to_file)

    def read_all(self, save=True):
        patients = self.get_patients()
        for patient in patients:
            patient = patients[2]
            print('Patient: ' + patient)
            weeks = self.get_weeks(patient, prt=False)
            for week in weeks:
                recordings_sessions = self.get_recording_sessions(patient_id=patient, week=week, prt=False)
                for recording_session in recordings_sessions:
                    recordings = self.get_recording_data(patient_id=patient, week=week,
                                                         recording_session=recording_session, prt=False)
                    for recording in recordings:
                        recording_path = self.get_recording_path(patient_id=patient, week=week,
                                                                 recording_session=recording_session)
                        recording_filename = glob(os.path.join(recording_path, recording))[-1]
                        samples = sw_util._load_data(filename=recording_filename)
                        pat_data = {'samples': samples,
                                    'date': samples.device_motion.date,
                                    'gravity': samples.device_motion.gravity,
                                    'heading': samples.device_motion.heading,
                                    'rotation_rate': samples.device_motion.rotation_rate,
                                    'acceleration': samples.device_motion.user_acceleration,
                                    'start_date': samples.start_date,
                                    'end_date': samples.end_date,
                                    'ID': samples.participant_id,
                                    'type': samples.DESCRIPTOR.full_name}
                        if save:
                            if 'phone' in recording:
                                np.save(self.save_path + 'phone/' + patient + '_' + week + '_' + recording + '.npy',
                                        pat_data)
                            else:
                                np.save(self.save_path + 'watch/' + patient + '_' + week + '_' + recording + '.npy',
                                        pat_data)


def main():
    # Define directories
    base_dir = glob('/Users/vicenteperissempere/Box/StopWatch-Data/data/')[-1]
    print(base_dir)

    save_dir = glob('/Users/vicenteperissempere/Box/Vicente Peris Sempere\'s Files/StopWatch-Data')[-1]
    print(save_dir)

    # Instance of data manager
    dataManager = DataManager(save_path=save_dir, base_dir=base_dir)

    # Print patients
    patients = dataManager.get_patients(prt=True)
    weeks = dataManager.get_weeks(patient_id=patients[0], prt=True)
    recordings_sessions = dataManager.get_recording_sessions(patient_id=patients[0], week=weeks[0], prt=True)
    recordings = dataManager.get_recording_data(patient_id=patients[0], week=weeks[0],
                                                recording_session=recordings_sessions[0], prt=True)

    # Read and save all
    dataManager.read_all(save=True)

if __name__ == '__main__':
    main()
