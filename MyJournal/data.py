import os
import time
from datetime import datetime as dt

import pandas as pd

class Data:
	DATA_PATH = '../data'

	def __init__(self, filename='myLog'):
		self.filename = filename
		self.path = f'{self.DATA_PATH}/{self.filename}.csv'

		self._df = pd.DataFrame()
		self._today = None

	@property
	def today(self):
		if self._today == None:
			self._today = dt.today()

		return self._today

	@property
	def now(self):
		return dt.today().strftime("%Y-%m-%d %H:%M:%S")

	@property
	def df(self):
		#create new DF if no filename and df is empty
		if not os.path.exists(self.path) and self._df.empty:
			self._df = pd.DataFrame(columns=['date', 'note']).set_index('date')

		#load filename
		elif self._df.empty:
			self._df = pd.read_csv(self.path).set_index('date')

		return self._df

	def write(self):
		self.df.to_csv(self.path)

	def new_entry(self, category, entry):
		self.df.loc[self.now, category] = entry


if __name__ == '__main__':
	d = Data('myLog')
	# d.new_entry('yoga', '20')
	# d.new_entry('note', 'This is a note')
	# d.write()
	# print(d.df)



