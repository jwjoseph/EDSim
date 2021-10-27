import scipy as sp
import numpy as np
import pandas as pd
import queue
import csv
import matplotlib.pyplot as plt


from ED import ED
from Patient import Patient
from Doctor import Doctor
from Laboratory import Laboratory
from Grapher import Grapher
from Stats import Stats
from Stats import Stats_Aggregator


def BernoulliTrial(probability):
    chance = random.uniform(0,1)
    if chance <= probability:
        return True
    return False

def arrival_record_from_csv():
	"""turn a csv file into a dictionary of arrival times for the simulation"""
	visitDict = {}

	with open('arrivals.csv', newline='') as f:
	    reader = csv.reader(f)
	    for row in reader:
	    	visitDict[row[0]]=row[1]

	return visitDict


## def __init__(self, ID_num, num_docs, doc_front_rate, doc_back_rate, patient_rate, department_size, waiting_size, admission_enabled=True, admit_rate,
##     labs_enabled=True, lab_rate=20, CT_enabled=True, num_CTs = 1, CT_rate=15, use_csv=False, verbose=True):
TotalStats = Stats_Aggregator()

choice = input("Run custom simulation (Y/N)?: ")
if choice == "N":
	for j in range(50):
		if j == 0:
			myED = ED(1, 2, 15, 5, 10, 20, 10, True, 20, True, 20, True, 1, 15, False, True)
			# demonstrate verbose output for one simulation only... then do the remaining 50 runs to average results
		else:
			myED = ED(1, 2, 15, 5, 10, 20, 10, True, 20, True, 20, True, 1, 15, False, False)

		for i in range(480):
		    myED.update()

		TotalStats.add_dataframe(myED.output_stats())

else:
	use_csv = input("Use custom arrivals file (Y/N): ")
	if use_csv == "Y":
		use_csv = True
	else:
		use_csv = False
	num_docs = int(input("Number of doctors (1-10): "))
	doc_front_rate = int(input("Average initial patient workup time in minutes (1-60): "))
	doc_end_rate = int(input("Average time to disposition an evaluated patient in minutes (1-60): "))

	if use_csv == False:
		patient_rate = int(input("Average number of patient arrivals per hour (1-60): "))
	else:
		patient_rate = 10 # default value

	#patient_rate = 60 // patient_rate
	department_size = int(input("Department size (1-200): "))
	waiting_size = int(input("Waiting room size (1-100): "))

	admission_enabled = input("Simulate admissions? (Y/N): ")
	if admission_enabled == "Y":
		admission_enabled = True
		admit_rate = int(input("Average wait in minutes for inpatient admission/transport (1-60): "))
	else:
		admission_enabled = False
		admit_rate = 1

	labs_enabled = input("Simulate lab times (Y/N): ")
	if labs_enabled == "Y":
		lab_rate = int(input("Average lab turnaround time in minutes (1-60): "))
		labs_enabled = True
	else:
		lab_rate = 20
		labs_enabled = False

	CT_enabled = input("Simulate CT scanner (Y/N): ")
	if CT_enabled == "Y":
		num_CTs = int(input("Number of CT scanners (1-10): "))
		CT_rate = int(input("Average CT imaging time in minutes (1-60): "))
		CT_enabled = True
	else:
		num_CTs = 1
		CT_rate = 15
		CT_enabled = False

	if use_csv == False:
		duration = int(input("Simulation duration in hours (1-72): "))
		duration = duration * 60

	## if pure simulation, no arrival record, go ahead and run the simulation
	if use_csv == False:
		for j in range(50):
			if j == 0:
				myED = ED(1, num_docs, doc_front_rate, doc_end_rate, patient_rate, department_size, waiting_size, admission_enabled, admit_rate, labs_enabled, lab_rate, CT_enabled, num_CTs, CT_rate, False, True)
			else:
				myED = ED(1, num_docs, doc_front_rate, doc_end_rate, patient_rate, department_size, waiting_size, admission_enabled, admit_rate, labs_enabled, lab_rate, CT_enabled, num_CTs, CT_rate, False, False)


			for i in range(duration):
			    myED.update()

			TotalStats.add_dataframe(myED.output_stats())

	## using an arrival record
	else:
		arrivals = arrival_record_from_csv()
		duration = len(arrivals)

		for j in range(50):
			if j == 0:
				myED = ED(1, num_docs, doc_front_rate, doc_end_rate, patient_rate, department_size, waiting_size, admit_rate, labs_enabled, lab_rate, CT_enabled, num_CTs, CT_rate, arrivals, True)
			else:
				myED = ED(1, num_docs, doc_front_rate, doc_end_rate, patient_rate, department_size, waiting_size, admit_rate, labs_enabled, lab_rate, CT_enabled, num_CTs, CT_rate, arrivals, False)


			for i in range(duration):
			    myED.update()

			TotalStats.add_dataframe(myED.output_stats())



TotalStats.merge_dataframes()
TotalStats.stats_total_to_file()

mygraph = Grapher()
mygraph.basic_graphs()


