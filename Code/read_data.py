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
import utils as sw_util
import matplotlib
from scripts import utils as UT

# Set directories

class DataManager:

    def read_data(self):
        filename = self.fileName



def main():

    # Define directories
    base_dir = glob('/Users/vicenteperissempere/Box/StopWatch-Data/')[-1]
    print(base_dir)

    # Add data directory
    data_dir = glob(os.path.join(base_dir, 'data/'))[-1]
    print(data_dir)

    # List files (patients and controls)
    files = os.listdir(data_dir)

    # Separate controls from patients
    patient_files = [file for file in files if file.isdigit()]
    control_files = [file for file in files if not file.isdigit()]
    print(patient_files)
    print(control_files)

    # Take patient data as test
    test = True
    if test:

        # Take the first patient
        patient = patient_files[0]
        print(patient)

        # Take records
        patient_records = os.listdir(glob(os.path.join(data_dir, patient))[-1])
        print(patient_records)

        # Take first week
        week_file = patient_records[0]

        # List files in the week
        week_dir = glob(os.path.join(data_dir, patient + '/' + week_file + '/'))[-1]
        print(os.listdir(week_dir))

        # Take first week record
        week_date = os.listdir(week_dir)[0]
        records_dir = glob(os.path.join(week_dir, week_date + '/'))[-1]
        records_files = os.listdir(records_dir)
        print(records_files)

        # Take data
        patient_data = glob(os.path.join(records_dir, records_files[1]))[-1]
        print(patient_data)

        samples = UT._load_data(patient_data)

        print('STOP')

if __name__ == '__main__':
    main()

