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


myED = ED(2, 12, 20, 10)

for i in range(200):
    myED.update()

myED.output_stats()


