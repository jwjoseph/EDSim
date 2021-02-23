class ED():
    def __init__(self, num_docs, doc_rate, patient_rate, department_size, waiting_size, admit_rate):
        self.erack = queue.PriorityQueue()
        self.rads_queue = queue.PriorityQueue()
        self.time = 0
        num_CTs = 1

        self.DoctorList = []
        self.CTList = []
        self.DispoList = []
        self.AdmitList = []
        self.patient_rate = patient_rate ## patient rate in terms of new patients per hour
        self.department_size = department_size
        self.waiting_size = waiting_size
        self.WR = queue.PriorityQueue(waiting_size)

        self.admit_rate = admit_rate ## average time in minutes to admit a patient
        self.doc_rate = doc_rate

        for i in range(num_docs):
            self.DoctorList.append(Doctor(self, 1, self.doc_rate, 8))

        for j in range(num_CTs):
            self.CTList.append(CT(self, 15))

        self.Laboratory = Laboratory(self, 20)
        self.LWBSCount = 0
        self.stats = Stats(num_docs, patient_rate, department_size, waiting_size)


    def get_time(self):
        """getter for children"""
        return self.time

    def dispoAdd(self, pt):
        """setter for dispolist - add pt"""
        self.DispoList.append(pt)

    def admitAdd(self, pt):
        """setter for dispolist - add pt"""
        self.AdmitList.append(pt)

    def dispoPop(self, pt):
        """setter for dispolist - rem pt"""
        # version 2 will need to delete
        print("Patient", pt.get_ID(), "discharged at time", self.get_time())
        self.DispoList.remove(pt)

    def admitPop(self, pt):
        print("Patient", pt.get_ID(), "admitted at time", self.get_time())
        self.AdmitList.remove(pt)

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
        """generate a patient based on a bernoulli process, place it if there's room...
        current behavior - patients LWBS when there is no room in the WR"""
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

    def send_patient_rads(self, patient):
        self.rads_queue.put(patient)

    def send_patient_CT(self):
        return self.rads_queue.get()

    def rads_empty(self):
        return self.rads_queue.empty()


    def admit_patient(self, patient):
        probability = np.random.uniform(0,1)
        if probability <= (self.admit_rate/60):
            patient.update()


    def output_stats(self):
        """output a csv of the stats to file from the ED's stats object"""
        output = self.stats.output()
        fieldnames = ["time", "waiting room", "in department", "to be seen"]
        with open('stats.csv','w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames)
            writer.writeheader()
            for key,val in sorted(output.items()):
                row = {'time': key}
                row.update(val)
                writer.writerow(row)
        
    def update(self):
        """main function for the MVC model. calls an update for every agent within the ED
        starts by checking whether to generate a patient, then runs an update for each agent
        finally outputs to stats"""
        print("Time:", self.time, "  In waiting room:", self.get_total_WR(), "  In department:", self.get_total_volume(), "  To be seen:", self.erack.qsize())
        self.generate_patient_prob()
        self.Laboratory.update()
        for ct in self.CTList:
            ct.update()
        for doc in self.DoctorList:
            doc.update()
        for pt in self.DispoList:
            pt.update()
        for pt in self.AdmitList:
            self.admit_patient(pt)
        self.update_WR_erack()
        self.stats.update(self.time,  self.WR.qsize(), self.get_volume(), self.erack.qsize())

        self.time += 1
        print()



import scipy as sp
import numpy as np
import queue
import csv

from Doctor import Doctor
from Patient import Patient
from Laboratory import Laboratory
from Stats import Stats
from CT import CT