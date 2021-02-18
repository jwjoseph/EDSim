class CT():
    ID = 0
    """Simulates a CT scanner. Sees patients with rads requests. For simplicity, has a single buffer,
        only accomodates one patient at a time!"""

    def __init__(self, ED, CT_rate):
        self.ED = ED
        self.CT_rate = CT_rate # average speed of a CT in number/hour
        self.IDnum = CT.ID
        CT.ID += 1
        self.ActivePt = None # only one at a time.
        print("CT", self.ID, "created.")

    def get_time(self):
        """getter for simulation time"""
        return self.ED.get_time()

    def get_ID(self):
        """getter for own ID"""
        return self.IDnum

    def get_next_patient(self):
        if not self.ED.rads_empty():
            newpatient = self.ED.send_patient_CT()
            self.ActivePt = newpatient
            print("Taking patient", self.ActivePt.get_ID(), "to CT", self.IDnum, "at", self.ED.get_time())

    def finish_patient_CT(self, patient):
        """on update, with successful lab copmletion, set patient's labs to done and remove from the lab queue"""
        patient.finish_rads()
        
        print("CT", self.IDnum, "finished scans for Patient", self.ActivePt.get_ID(), "at", self.ED.get_time())
    
    def update(self):
        """check if patients need labs, if so, add to queue. if labs finish for a patient, set them to done and
        take them out of the queue"""
        print("CT", self.IDnum, ": Active Patient: ", end="")
        if self.ActivePt is not None:
            print(self.ActivePt.get_ID(), end=" ")

            probability = np.random.uniform(0,1)
            if probability <= (self.CT_rate/60):
                self.finish_patient_CT(self.ActivePt)
                self.ActivePt = None

        else:
            self.get_next_patient()

        print()

        return




import scipy as sp
import numpy as np
import queue

from ED import ED
from Patient import Patient