class Stats():
	def __init__(self, num_docs, patient_rate, department_size, waiting_size):
		self.record = dict()
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

	def update(self, time,  wr_total,  dept_total, erack_total):
		self.record[time] = {"waiting room": wr_total, "in department": dept_total, "to be seen": erack_total, "average wait time": self.average_waiting_time, "average door2doc time": self.average_d2d_time, "average LOS": self.average_LOS}

	def output_times(self, time):
		print("Average wait time:", self.record[time]["average wait time"], "Average door2doc time:", self.record[time]["average door2doc time"], "Average LOS:", self.record[time]["average LOS"])

	def output(self):
		"""return the dictionary"""
		return self.record



import scipy as sp
import numpy as np
import csv
import matplotlib.pyplot as plt

from ED import ED
from Patient import Patient
from Patient import Patient
from Laboratory import Laboratory