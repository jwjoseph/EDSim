class Stats():
	def __init__(self, num_docs, patient_rate, department_size, waiting_size):
		self.record = dict()
		self.num_docs = num_docs
		self.department_size = department_size
		self.waiting_size = waiting_size

	def update(self, time,  wr_total,  dept_total, erack_total):
		self.record[time] = {"waiting room": wr_total, "in department": dept_total, "to be seen": erack_total}

	def output(self):
		"""return the dictionary"""
		return self.record



import scipy as sp
import numpy as np
import csv

from ED import ED
from Patient import Patient
from Patient import Patient
from Laboratory import Laboratory