import os
from datetime import datetime as dt

import pandas as pd

class Data:
	DATA_PATH = '../data'

	def __init__(self, filename):
		self.filename = filename
		self.path = f'{self.DATA_PATH}/{self.filename}.csv'

		self._df = pd.DataFrame()
		self._today = None

	@property
	def today(self):
		if self._today == None:
			self._today = dt.today().date()

		return self._today

	@property
	def df(self):
		#create new DF if no filename and df is empty
		if not os.path.exists(self.path) and self._df.empty:
			self._df = pd.DataFrame()

		#load filename
		elif self._df.empty:
			self._df = pd.read_csv(self.path)

		return self._df

	def write(self):
		self.df.to_csv(self.path)

	def new_entry(self, category, entry):
		self.df.loc[self.today, category] = entry


if __name__ == '__main__':
	d = Data('namea')
	d.new_entry('run', '6km')
	d.new_entry('run', '65km')
	print(d.df)






