class Grapher():
	def __init__(self):
		self.df = pd.read_csv('stats.csv')

	def basic_graphs(self):
		fig, axs = plt.subplots(2, 2)
		axs[0, 0].plot(self.df['time'],self.df['waiting room'])
		axs[0, 0].set_title('Avg Waiting Room Volume')
		axs[0, 0].set_ylabel('Volume')

		axs[0, 1].plot(self.df['time'],self.df['average wait time'], 'tab:orange')
		axs[0, 1].set_title('Average Wait Time')
		axs[0, 1].set_ylabel('Time (min)')

		axs[1, 0].plot(self.df['time'],self.df['average door2doc time'], 'tab:green')
		axs[1, 0].set_title('Average Door to Doc Time')		
		axs[1, 0].set_ylabel('Time (min)')

		axs[1, 1].plot(self.df['time'],self.df['average LOS'], 'tab:red')
		axs[1, 1].set_title('Average LOS')
		axs[1, 1].set_ylabel("LOS (min)")

		for ax in axs.flat:
		    ax.set(xlabel='simulation time')

		plt.tight_layout()

		plt.show()


import scipy as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt