class Stats():
    def __init__(self, num_docs, patient_rate, department_size, waiting_size):
        self.record = dict()
        self.record["ID"] = []
        self.record["time"] = []
        self.record["waiting room"] = []
        self.record['in department'] = []
        self.record['to be seen'] = []
        self.record['average wait time'] = []
        self.record['average door2doc time'] = []
        self.record['average LOS'] = []



        self.num_docs = num_docs
        self.department_size = department_size
        self.waiting_size = waiting_size
        self.total_patients = 0 # total patients generated

        self.total_waiting_time = 0 # total amount of time waited by patients
        self.total_patients_waited = 0 # total number of patients brought in from WR
        self.average_waiting_time = 0
        
        self.total_to_be_seen_time = 0 # total time patients have waited to be seen
        self.total_patients_seen = 0 # total number of patients who have been seen
        self.average_d2d_time = 0

        self.total_LOS = 0 # total amount of time in system
        self.total_patients_dispo = 0 # total number of patients dispositioned
        self.average_LOS = 0

        self.LWBS = 0

    def update_total_patients(self):
        """adds a patient to the total"""
        self.total_patients += 1

    def update_LWBS(self):
        """add a patient to the LWBS total"""
        self.LWBS += 1


    def update_waiting_time(self, time):
        """increase the aggregate waiting time, update the average"""
        self.total_waiting_time += time
        self.total_patients_waited += 1
        self.average_waiting_time = round(self.total_waiting_time / self.total_patients_waited, 2)

    def update_to_be_seen_time(self, time):
        """increase the aggregate to be seen time, update the average"""
        self.total_to_be_seen_time += time
        self.total_patients_seen += 1
        self.average_d2d_time = round(self.total_to_be_seen_time / self.total_patients_seen, 2)

    def update_LOS(self, time):
        """increase the aggregate LOS time, update the average"""
        self.total_LOS += time
        self.total_patients_dispo += 1
        self.average_LOS = round(self.total_LOS / self.total_patients_dispo, 2)

    def update(self, ID, time,  wr_total,  dept_total, erack_total):
        self.record["ID"].append(ID)
        self.record["time"].append(time)
        self.record["waiting room"].append(wr_total)
        self.record['in department'].append(dept_total)
        self.record['to be seen'].append(erack_total)
        self.record['average wait time'].append(self.average_waiting_time)
        self.record['average door2doc time'].append(self.average_d2d_time)
        self.record['average LOS'].append(self.average_LOS)

    def output_times(self, time):
        print("Average wait time:", self.record["average wait time"][time], "Average door2doc time:", self.record["average door2doc time"][time], "Average LOS:", self.record["average LOS"][time])

    def output(self):
        """return the dictionary"""
        return self.record

    def output_stats(self):
        """return a dataframe of the stats"""
        fieldnames = ["time", "waiting room", "in department", "to be seen", "average wait time", "average door2doc time", "average LOS"]
        data = pd.DataFrame({"ID":self.record["ID"],
            "time":self.record["time"],
            "waiting room": self.record["waiting room"],
            "in department": self.record['in department'],
            "to be seen": self.record['to be seen'],
            "average wait time": self.record['average wait time'],
            "average door2doc time": self.record['average door2doc time'],
            "average LOS": self.record['average LOS']},)
        data.set_index('time')
        return data

    def stats_to_file(self):
        """send dataframe to csv"""
        data = self.output_stats()
        data.to_csv('stats.csv',)


class Stats_Aggregator():
    def __init__(self):
        self.dfs = []

    def add_dataframe(self, df):
        self.dfs.append(df)

    def merge_dataframes(self):
        self.main_df = pd.concat(self.dfs).groupby(level=0).mean()

    def stats_total_to_file(self):
        self.main_df.to_csv('stats.csv')

import scipy as sp
import numpy as np
import pandas as pd
import csv

from ED import ED
from Patient import Patient
from Laboratory import Laboratory