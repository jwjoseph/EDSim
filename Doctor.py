class Doctor():
    ID = 0
    """Simulates a doctor. Sees patients from an erack,can handle maxPts at a time"""
    def __init__(self, ED, pickup_rate, eval_rate, dispo_rate, maxPts):
        self.ED = ED
        self.erack = ED.erack
        self.pickup_rate = pickup_rate # willingness to pick up a free patient (0-1)
        self.eval_rate = eval_rate # speed of initial eval (minutes)
        self.dispo_rate = dispo_rate # speed of disposition after eval (minutes)
        self.IDnum = Doctor.ID
        Doctor.ID += 1
        self.NewPts = queue.Queue(1) # signed up, to be seen, currently capped at 1, but will be on priority - can bump for acute pt
        self.ActivePts = [] # list - everyone in it is waiting on something
        self.DispoPts = [] # currently can handle a lot of signout or dispo-ed patients
        self.currentPt = None # for the sake of simulation, only doing one H&P/action at a time, w/o interruption
        if self.ED.get_verbose():
            print("Doctor", self.IDnum, "created.")

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
                if self.ED.get_verbose():
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
        """if there is an active patient with stuff to do, return them, else none - dispo comes first"""
        for patient in self.ActivePts:
            if patient.get_state() == "evaluated":
                if patient.has_needs():
                    pass
                else:
                    return patient
            else:
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
            if self.ED.get_verbose():
                print("Doctor", self.IDnum, ": Evaluating patient", self.currentPt.get_ID() ,"at", self.get_time())
            self.currentPt.MDupdate()
            return
            
        elif to_do == "evaluating":
            probability = np.random.uniform(0,1)
            evals_hour = 60 / self.eval_rate
            if probability <= (evals_hour / 60):
                if self.ED.get_verbose():
                    print("Doctor", self.IDnum, ": finished evaluating patient", self.currentPt.get_ID() ,"at", self.get_time())
                self.currentPt.MDupdate()
                self.currentPt = None
                self.lastActionTimer = 0
                return
            else:
                return
        elif to_do == "treated":
            ## dispo pt
            probability = np.random.uniform(0,1)
            dispos_hour = 60 / self.dispo_rate
            if probability <= (dispos_hour / 60):
                if self.ED.get_verbose():
                    print("Doctor", self.IDnum, ": dispositioning patient", self.currentPt.get_ID() ,"at", self.get_time())
                self.currentPt.MDupdate()
                self.DispoPts.append(self.currentPt)
                self.ActivePts.remove(self.currentPt)
                self.currentPt = None
        else:
            self.currentPt.MDupdate()
            self.currentPt = None
    
    def update(self):
        """General behavior - if not currently working on a patient:
        1. Check if anyone in the active list can be dispositioned # dispo takes priority
        2. Check if there is a new patient to see
        3. Otherwise, pass
        """
        if self.currentPt is None: # not actively working on a patient -- use not None as == is overloaded for comp
            self.lastActionTimer = 0 # reset
            self.currentPt == self.get_next_patient_action()

        else:
            self.eval_treat_patient()

        if self.ED.get_verbose():
            print("Doctor", self.IDnum, ":", end=" ")
            print("Current patient:", end=" ")
            if self.currentPt is not None:
                print(self.currentPt.get_ID(), ":", self.currentPt.get_state(), end=" ")
            print()
            print("    Active Patients: ", end=" ")
            for pt in self.ActivePts:
                if pt.get_state() != "evaluated":
                    print(pt.get_ID(), pt.get_state(), end="  ")
                else:
                    print(pt.get_ID(), "evaluated|needs:", pt.get_needs(), end="  ")
            print()
            print("    Dispositioned Patients: ", end=" ")
            for pt in self.DispoPts:
                print(pt.get_ID(), pt.get_state(), end=" ")
            print()


        return




import scipy as sp
import numpy as np
import queue

from ED import ED
from Patient import Patient