class Patient():
    ID = 0
    def __init__(self, ED, ESI):
        self.ED = ED # can call parent object to get timestamps
        self.ESI = ESI
        self.startTime = ED.get_time()
        self.ID = Patient.ID
        self.state = "unassigned" # states = unassigned, assigned, evaluated, treated, dispositioned
        self.needs = set() # labs, rads, meds, etc.
        self.doc = None
        self.needs_admit = False

        self.d2doc_time = 0
        self.wr_time = 0
        self.doc2dec_time = 0
        self.LOS = 0

        Patient.ID += 1
        print("Patient", self.ID, ": I have arrived at time ", self.startTime)

        # Based on ESI, generate a likelihood of needing labs, radiology, admission
        ESIdict = {1:[0.9, 0.0, 0.8], 2:[0.8, 0.0, 0.6], 3:[0.75, 0.0, 0.4], 4:[0.5, 0.0, 0.2], 5:[0.3, 0.0, 0.1]}
        if np.random.uniform(0,1) <= ESIdict[self.ESI][0]:
            self.needs.add("labs")
        #if np.random.uniform(0,1) <= ESIdict[self.ESI][1]:
        #    self.needs.add("rads")
        if np.random.uniform(0,1) <= ESIdict[self.ESI][2]:
            self.needs_admit = True

    def get_state(self):
        return self.state

    def get_ID(self):
        return self.ID

    def has_needs(self):
        return len(self.needs) > 0

    def set_doc(self, newdoc):
        self.doc = newdoc

    def finish_labs(self):
        if "labs" in self.needs:
            self.needs.remove("labs")
        #self.MDupdate()

    def finish_rads(self):
        if "rads" in self.needs:
            self.needs.remove("rads")
    

    def MDupdate(self):
        """state changes due to MD"""
        if self.state == "unassigned":
            self.d2doc_time = self.ED.get_time() - self.startTime
            self.state = "assigned"

        elif self.state == "assigned":
            if len(self.needs) < 1:
                self.state = "treated"
                #print("Patient", self.ID, ": fully treated at time ", self.startTime) ##debug
            else:
                self.state = "evaluated"
                if "labs" in self.needs:
                    self.ED.send_patient_labs(self)

        elif self.state == "evaluated":
            # hang out until needs are met
            if len(self.needs) == 0:
                self.state = "treated"

        elif self.state == "treated":
            self.state = "dispositioned"
            self.doc2dec_time = self.ED.get_time() - self.d2doc_time
            self.ED.dispoAdd(self)

    def update(self):
        """state (and other) changes due to simulation time"""
        print("Patient", self.ID, self.state, "at time", self.ED.get_time())
        if self.state == "dispositioned":
            self.LOS = self.ED.get_time() - self.startTime
            self.doc.DispoPts.remove(self)
            self.ED.dispoPop(self)



## changed from original priorityqueue ESI definitions
    def __lt__(self, other):
        # p1 < p2 calls p1.__lt__(p2)
        return self.ID > other.ID
    
    def __eq__(self, other):
        # p1 == p2 calls p1.__eq__(p2)
        return self.ID == other.ID

    def __gt__(self, other):
        # p1 < p2 calls p1.__lt__(p2)
        return self.ID < other.ID

    def __repr__(self):
        return self.ID

import scipy as sp
import numpy as np
import queue

from Doctor import Doctor
from ED import ED