class ED():
    def __init__(self, num_docs, patient_rate, department_size, waiting_size):
        self.erack = queue.PriorityQueue()
        self.time = 0
        self.DoctorList = []
        self.DispoList = [] # this will need to get split to admit/dc
        self.patient_rate = patient_rate ## patient rate in terms of patients per hour
        self.department_size = department_size
        self.waiting_size = waiting_size
        self.WR = queue.PriorityQueue(waiting_size)
        for i in range(num_docs):
            self.DoctorList.append(Doctor(self, 1, 10, 8))
        self.Laboratory = Laboratory(self, 20)
        self.LWBSCount = 0


    def get_time(self):
        """getter for children"""
        return self.time

    def dispoAdd(self, pt):
        """setter for dispolist - add pt"""
        self.DispoList.append(pt)

    def dispoPop(self, pt):
        """setter for dispolist - rem pt"""
        # version 2 will need to delete
        self.DispoList.remove(pt)

    def get_volume(self):
        total = self.erack.qsize()
        for doc in self.DoctorList:
            total += doc.get_patient_totals()
        return total

    def get_total_volume(self):
        return str(self.get_volume()) + " / " + str(self.department_size)

    def get_total_WR(self):
        """returns a string of the waiting room volume vs. capacity"""
        return str(self.WR.qsize()) + " / " + str(self.waiting_size)

    def generate_patient_prob(self):
        """generate a patient based on a bernoulli process, place it if there's room..."""
        probability = np.random.uniform(0,1)
        if probability <= (self.patient_rate / 60):
            # a patient was generated
            if self.get_volume() < self.department_size:
                self.erack.put(Patient(self, 3))
            elif self.WR.qsize() < self.waiting_size:
                self.WR.put(Patient(self, 3))
            else:
                newpt = Patient(self, 3)
                print("Patient", newpt.get_ID(), "left without being seen!")
                self.LWBSCount += 1

    def update_WR_erack(self):
        """check if patients can be brought from the WR to the erack"""
        if self.get_volume() < self.department_size:
            if not self.WR.empty():
                newpt = self.WR.get()
                self.erack.put(newpt)

    def send_patient_labs(self, patient):
        self.Laboratory.get_next_patient(patient)
        
    def update(self):
        print("Time:", self.time, "  In waiting room:", self.get_total_WR(), "  In department:", self.get_total_volume(), "  To be seen:", self.erack.qsize())
        self.generate_patient_prob()
        self.Laboratory.update()
        for doc in self.DoctorList:
            doc.update()
        for pt in self.DispoList:
            pt.update()
        self.update_WR_erack()

        self.time += 1
        print()



import scipy as sp
import numpy as np
import queue

from Doctor import Doctor
from Patient import Patient
from Laboratory import Laboratory