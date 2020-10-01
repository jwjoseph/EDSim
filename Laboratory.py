class Laboratory():
    ID = 0
    """Simulates a laboratory. Sees patients with lab requests. For simplicity, has an infinite queue.
        Note that the queue accomodates MULTIPLE simultaneous patients"""
    def __init__(self, ED, lab_rate):
        self.ED = ED
        self.erack = ED.erack
        self.lab_rate = lab_rate # average speed of a lab test in number/hour
        self.IDnum = Laboratory.ID
        Laboratory.ID += 1
        self.ActivePts = [] # dict - everyone in it is waiting on something
        print("Laboratory", self.ID, "created.")

    def get_time(self):
        """getter for simulation time"""
        return self.ED.get_time()

    def get_ID(self):
        """getter for own ID"""
        return self.IDnum

    def get_patient_totals(self):
        """getter for total patients in lab queue"""
        return len(self.ActivePts)


    def get_next_patient(self, patient):
        """adds a patient to the lab buffer. called by the ED to put a new patient into the lab queue."""
        self.ActivePts.append(patient)
        print("Sending labs for Patient", patient.get_ID(), "at", self.ED.get_time())

    def finish_patient_labs(self, patient):
        """on update, with successful lab copmletion, set patient's labs to done and remove from the lab queue"""
        patient.finish_labs()
        self.ActivePts.remove(patient)
        print("Laboratory", self.IDnum, "finished labs for Patient", patient.get_ID(), "at", self.ED.get_time())

    
    def update(self):
        """check if patients need labs, if so, add to queue. if labs finish for a patient, set them to done and
        take them out of the queue"""
        print("Lab", self.IDnum, ": Active Patients: ", end="")
        for pt in self.ActivePts:
            print(pt.get_ID(), end=" ")
        print()

        for patient in self.ActivePts:
            probability = np.random.uniform(0,1)
            if probability <= ((self.lab_rate)/60):
                self.finish_patient_labs(patient)

        return




import scipy as sp
import numpy as np
import queue

from ED import ED
from Patient import Patient