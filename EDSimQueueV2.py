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


myED = ED(2, 15, 10, 20, 10, 20)

for i in range(480):
    myED.update()

myED.output_stats()


