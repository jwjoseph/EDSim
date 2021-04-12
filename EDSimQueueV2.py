import scipy as sp
import numpy as np
import queue

from ED import ED
from Patient import Patient
from Doctor import Doctor
from Laboratory import Laboratory


def BernoulliTrial(probability):
    chance = random.uniform(0,1)
    if chance <= probability:
        return True
    return False



## def __init__(self, num_docs, doc_rate, patient_rate, department_size, waiting_size, admit_rate, labs_enabled=True, lab_rate=20, CT_enabled=True, num_CTs = 1, CT_rate=15):

choice = input("Run custom simulation (Y/N)?: ")
if choice == "N":
	myED = ED(2, 15, 10, 20, 10, 20, True, 20, True, 1, 15)

	for i in range(480):
	    myED.update()
else:
	num_docs = int(input("Number of doctors (1-10): "))
	doc_rate = int(input("Average patient workup time in minutes (1-60): "))
	patient_rate = int(input("Average number of patient arrivals per hour (1-60): "))
	#patient_rate = 60 // patient_rate
	department_size = int(input("Department size (1-100): "))
	waiting_size = int(input("Waiting room size (1-100): "))
	admit_rate = int(input("Average wait in minutes for inpatient transport (1-60): "))
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

	duration = int(input("Simulation duration in hours (1-72): "))
	duration = duration * 60

	myED = ED(num_docs, doc_rate, patient_rate, department_size, waiting_size, admit_rate, labs_enabled, lab_rate, CT_enabled, num_CTs, CT_rate)

	for i in range(duration):
	    myED.update()

myED.output_stats()


