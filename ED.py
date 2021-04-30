class ED():
    def __init__(self, num_docs, doc_rate, patient_rate, department_size, waiting_size, admit_rate, labs_enabled=True, lab_rate=20, CT_enabled=True, num_CTs = 1, CT_rate=15, verbose=True):
        self.erack = queue.PriorityQueue()
        self.rads_queue = queue.PriorityQueue()
        self.time = 0
        self.num_CTs = num_CTs
        self.CT_rate = CT_rate
        self.lab_rate = lab_rate
        self.num_docs = num_docs
        self.labs_enabled = labs_enabled
        self.CT_enabled = CT_enabled

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

        self.verbose = verbose ## use debug / status messages

        for i in range(self.num_docs):
            self.DoctorList.append(Doctor(self, 1, self.doc_rate, 8))


        if self.CT_enabled:
            for j in range(self.num_CTs):
                self.CTList.append(CT(self, self.CT_rate))

        if self.labs_enabled:
            self.Laboratory = Laboratory(self, self.lab_rate)

        self.stats = Stats(num_docs, patient_rate, department_size, waiting_size)


    def get_time(self):
        """getter for children"""
        return self.time

    def get_time_pretty(self):
        """return time in hours:minutes, let default be 0700"""
        hours = 7 + (self.get_time() // 60) % 24 
        minutes = self.get_time() % 60
        return str(hours) + ":" + str(minutes)

    def get_labs_enabled(self):
        return self.labs_enabled

    def get_CT_enabled(self):
        return self.CT_enabled

    def set_patient_rate(self, rate):
        """update pph"""
        self.patient_rate = rate

    def dispoAdd(self, pt):
        """setter for dispolist - add pt"""
        self.DispoList.append(pt)

    def admitAdd(self, pt):
        """setter for dispolist - add pt"""
        self.AdmitList.append(pt)

    def dispoPop(self, pt):
        """setter for dispolist - rem pt"""
        # version 2 will need to delete
        if self.get_verbose():
            print("Patient", pt.get_ID(), "discharged at time", self.get_time())
        LOS_time = pt.get_LOS()
        self.stats.update_LOS(LOS_time)
        self.DispoList.remove(pt)

    def admitPop(self, pt):
        if self.get_verbose():
            print("Patient", pt.get_ID(), "admitted at time", self.get_time())
        LOS_time = pt.get_LOS()
        self.stats.update_LOS(LOS_time)
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
                if self.get_verbose():
                    print("Patient", newpt.get_ID(), "left without being seen!")
                self.stats.update_LWBS()

    def update_WR_erack(self):
        """check if patients can be brought from the WR to the erack"""
        if self.get_volume() < self.department_size:
            if not self.WR.empty():
                newpt = self.WR.get()
                self.erack.put(newpt)
                newpt.set_WR_time()
                wait_time = newpt.get_LOS()
                self.stats.update_waiting_time(wait_time)

    def send_patient_labs(self, patient):
        self.Laboratory.get_next_patient(patient)

    def send_patient_rads(self, patient):
        self.rads_queue.put(patient)

    def send_patient_CT(self):
        return self.rads_queue.get()

    def rads_empty(self):
        return self.rads_queue.empty()


    def admit_patient(self, patient):
        """admits a patient who is waiting on admission - later update based on capacity"""
        probability = np.random.uniform(0,1)
        admit_time = 60/self.admit_rate
        if probability <= (admit_time/60):
            patient.update()


    def output_stats(self):
        """output a csv of the stats to file from the ED's stats object"""
        output = self.stats.output()
        fieldnames = ["time", "waiting room", "in department", "to be seen", "average wait time", "average door2doc time", "average LOS"]
        with open('stats.csv','w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames)
            writer.writeheader()
            for key,val in sorted(output.items()):
                row = {'time': key}
                row.update(val)
                writer.writerow(row)

    def get_verbose(self):
        return self.verbose

        
    def update(self):
        """main function for the MVC model. calls an update for every agent within the ED
        starts by checking whether to generate a patient, then runs an update for each agent
        finally outputs to stats"""
        if self.get_verbose():
            print("Time:", self.get_time_pretty(), "(" + str(self.get_time()) + ")" "  In waiting room:", self.get_total_WR(), "  In department:", self.get_total_volume(), "  To be seen:", self.erack.qsize())
        self.generate_patient_prob()
        if self.labs_enabled:
           self.Laboratory.update()

        if self.CT_enabled:
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
        self.stats.output_times(self.time)

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