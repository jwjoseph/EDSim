class Doctor():
    ID = 0
    """Simulates a doctor. Sees patients from an erack,can handle maxPts at a time"""
    def __init__(self, ED, pickup_rate, eval_rate, maxPts):
        self.ED = ED
        self.erack = ED.erack
        self.pickup_rate = pickup_rate # willingness to pick up a free patient (0-1)
        self.eval_rate = eval_rate # speed of initial eval (minutes)
        self.IDnum = Doctor.ID
        Doctor.ID += 1
        self.NewPts = queue.PriorityQueue(1) # signed up, to be seen, currently capped at 1, but will be on priority - can bump for acute pt
        self.ActivePts = [] # list - everyone in it is waiting on something
        self.DispoPts = [] # currently can handle a lot of signout or dispo-ed patients
        self.currentPt = None # for the sake of simulation, only doing one H&P/action at a time, w/o interruption
        self.lastActionTimer = 0
        print("Doctor", self.ID, "created.")

    def get_time(self):
        return self.ED.get_time()

    def get_ID(self):
        return self.IDnum

    def get_patient_totals(self):
        return len(self.ActivePts) + len(self.DispoPts) + self.NewPts.qsize()

    def get_patient_from_rack(self):
        """if there is a patient to get from rack, get them and add to NewPts"""
        if not self.erack.empty():
            if np.random.uniform(0,1) <= self.pickup_rate:
                newpatient = self.erack.get()
                self.NewPts.put(newpatient)
                print("Doctor", self.IDnum, ": Signed up for Patient", newpatient.get_ID(), "at", self.get_time())
                newpatient.set_doc(self)
                return newpatient
        return None

    def get_patient_from_new(self):
        """returns patient from newPts queue, none if empty"""
        if self.NewPts.empty():
            return None
        else:
            newpt = self.NewPts.get()
            self.ActivePts.append(newpt)
            return newpt

    def active_patient_need(self):
        """if there is an active patient with stuff to do, return them, else none"""
        for patient in self.ActivePts:
            if patient.get_state() != "evaluated":
                ### evaluated == already evaled, NTD for MD
                return patient
        return None

    def get_active_patients(self):
        return self.ActivePts


    def get_next_patient_action(self):
        """get the next patient task and set as the current patient if so
        1. Any active patients need next step? 
        2. If NTD, get a new patient
        3. else pass
        """
        if self.currentPt is not None:
            # sanity check
            return

        self.currentPt = self.active_patient_need() # if next patient is an existing pt, select them
        if self.currentPt is None:
            if not self.NewPts.full():
                self.get_patient_from_rack()  ## claim a patient from the erack, only an issue if allowing batches
            else:
                self.currentPt = self.get_patient_from_new()
        pass


    def eval_treat_patient(self):
        """update status of current patient - see pt, eval pt, dispo pt..."""
        # states = unassigned, assigned, evaluated, treated, dispositioned
        to_do = self.currentPt.get_state()
        if to_do == "assigned":
            ## initial eval
            if self.lastActionTimer < self.eval_rate:
                if self.lastActionTimer == 0:
                    print("Doctor", self.IDnum, ": Evaluating patient", self.currentPt.get_ID() ,"at", self.get_time())
                self.lastActionTimer += 1
                return
            elif self.lastActionTimer >= self.eval_rate:
                print("Doctor", self.IDnum, ": finished evaluating patient", self.currentPt.get_ID() ,"at", self.get_time())
                self.currentPt.MDupdate()
                self.currentPt = None
                self.lastActionTimer = 0
                return
        elif to_do == "treated":
            ## dispo pt
            print("Doctor", self.IDnum, ": dispositioning patient", self.currentPt.get_ID() ,"at", self.get_time())
            self.currentPt.MDupdate()
            self.ActivePts.remove(self.currentPt)
            self.DispoPts.append(self.currentPt)
            self.currentPt = None
        else:
            self.currentPt.MDupdate()
            self.currentPt = None
    
    def update(self):
        """General behavior - if not currently working on a patient:
        1. Check if anyone in the active list can be dispositioned
        2. Check if there is a new patient to see
        3. Otherwise, pass
        """
        print("Doctor", self.IDnum, ": Active Patients: ", end="")
        for pt in self.ActivePts:
            print(pt.get_ID(), end=" ")
        print()

        if self.currentPt is None: # not actively working on a patient -- use not None as == is overloaded for comp
            self.lastActionTimer = 0 # reset
            self.currentPt == self.get_next_patient_action()

        else:
            self.eval_treat_patient()

        return




import scipy as sp
import numpy as np
import queue

from ED import ED
from Patient import Patient