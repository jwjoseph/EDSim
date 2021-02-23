import scipy as sp
import numpy as np
import queue
import csv

### Toy simulation looking at CT utilization ratios

class ED():
    def __init__(self, patient_rate, num_CTs, CT_rate, mode="simple"):
        self.time = 0
        self.num_CTs = num_CTs
        self.CT_rate = CT_rate
        self.mode = mode

        self.CTList = []
        self.PTList = []

        self.total_waiting_CT = 0
        self.total_pts_finished = 0

        self.patient_rate = patient_rate ## patient rate in terms of new patients per hour

        for i in range(num_CTs):
            self.CTList.append(CT(self, CT_rate))


    def get_time(self):
        """getter for children"""
        return self.time

    def get_next_patient(self):
        if len(self.PTList) > 0:
            newpt = self.PTList.pop()
            return newpt
        else:
            return None

    def generate_patient_prob(self):
        """generate a patient based on a bernoulli process, place it if there's room...
        current behavior - patients LWBS when there is no room in the WR"""
        probability = np.random.uniform(0,1)
        if probability <= (self.patient_rate / 60):
            self.PTList.append(Patient(self))

    def finish_patient(self, patient):
        self.total_pts_finished += 1

    def get_avg_wait(self):
        if self.total_pts_finished > 0:
            return round(self.total_waiting_CT / self.total_pts_finished, 1)
        else:
            return 0

    def get_utilization_ratio(self):
        return round(self.patient_rate / (self.num_CTs * self.CT_rate), 2)

        
    def update(self):
        """main function for the MVC model. calls an update for every agent within the ED
        starts by checking whether to generate a patient, then runs an update for each agent
        """

        self.generate_patient_prob()

        for pt in self.PTList:
            pt.update()
            self.total_waiting_CT += 1

        for ct in self.CTList:
            ct.update()
 
        self.time += 1
        if self.mode == "rich":
            print("Time:", self.time, "Patients waiting:", len(self.PTList), "Average wait time: ", self.get_avg_wait())
            print()



class Patient():
    def __init__(self, ED):
        self.ED = ED
        self.start_time = self.ED.get_time()
        self.waiting_time = 0

    def get_waiting(self):
        return self.waiting_time

    def update(self):
        self.waiting_time += 1

class CT():
    def __init__(self, ED, CT_rate):
        self.ED = ED
        self.CT_rate = CT_rate
        self.current_patient = None

    def update(self):
        if self.current_patient == None:
            self.current_patient = self.ED.get_next_patient()
        else:
            probability = np.random.uniform(0,1)
            if probability <= (self.CT_rate / 60):
                self.ED.finish_patient(self.current_patient)
                self.current_patient = None

class Stats():
    def __init__(self):
        self.num_runs = 0
        self.aggregate_wait = 0

    def add_run(self, avg_wait_time):
        self.num_runs += 1
        self.aggregate_wait += avg_wait_time

    def total(self):
        return (round(self.aggregate_wait / self.num_runs, 2), self.num_runs)

if __name__ == "__main__":

    mystats = Stats()
    sim_length = 480

    for i in range(100):
        theED = ED(10, 1, 10)

        for i in range (sim_length):
            theED.update()

        mystats.add_run(theED.get_avg_wait())


    print("Average wait time for CT:", mystats.total()[0], "minutes per patient, calculated over", mystats.total()[1], "runs of", sim_length, "minutes.")
    print("Utilization ratio: ", theED.get_utilization_ratio())

