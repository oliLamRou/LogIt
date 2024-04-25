import pandas as pd 
import os
from pprint import pprint
import time
import datetime


class Tracking:

	path = "~/Documents/tracking/trackingData.csv"

	def __init__(self):
		#Set the day
		self.today = str(datetime.datetime.today().date())

		#Load file if doesn't exist create Date columns + current day  
		try:
			print("Loading file")
			self.DF = pd.read_csv(self.path)
		except:
			print("no file")
			self.DF = pd.DataFrame([self.today], columns=["Date"])

		# #If self.today not in Date -> Add it
		if self.today in self.DF["Date"].to_list():
			print("Not a new day")
		else:
			self.DF = self.DF.append({"Date": self.today}, ignore_index=True)
			
		#Set the today index
		self.todayIndex = self.DF.index[-1]


	def save_to_disk(self):
		self.DF.to_csv(self.path, index=False)

	def print_columns(self):
		i = 1
		catList = self.DF.columns.to_list()
		if len(catList) > 1:
			for i in range(1, len(catList)):
				print(str(i)+": ", catList[i])
		else:
			print("There is no category yet :( \n")

	def add_data(self, columns_index, value, index=None):
		#Get column name base on index
		columnName = self.DF.columns.to_list()[columns_index]

		#If index is default then set to today
		#Later useful to change the past
		if index == None:
			index = self.todayIndex
		else:
			pass

		#Change a single value
		self.DF[columnName][index] = value


	def ask_for_new_data(self):
		categoryList = list(self.DF.columns)

		os.system('cls||clear')
		# if there is more then Date category
		if len(categoryList) > 1:
			self.print_columns()
			columns_index = int(input("Which category you want to update?"))
			os.system('cls||clear')
			value = input("What do you want to say for {}?\n".format(self.DF.columns.to_list()[columns_index]))
			self.add_data(columns_index, value)
		else:
			#No category to add date
			print("There is no category")
			input("\nPress enter to continue")


	def ask_for_new_category(self):
		os.system('cls||clear')
		print("Current category:")
		self.print_columns()

		a = input("What category you want to add? \n")
		self.DF[a] = ""

	def delete_column(self):
		self.print_columns()
		columns_index = int(input("\nWhich columns you want to delete?"))
		columnName = self.DF.columns.to_list()[columns_index]
		self.DF.drop(columns=columnName, inplace=True)

	def show_chart(self):
		os.system('cls||clear')
		print(self.DF)
		input("\nPress enter to continue")


newTracking = Tracking()
x = newTracking


while True:
	os.system('cls||clear')
	print("1: Add new data")
	print("2: Add new category")
	print("3: Show Data")
	print("4: Save")
	print("5: Delete category")		
	print("6: Quit")
	a = input("What do you want?")


	if a == "1":
		newTracking.ask_for_new_data()
	elif a == "2":
		newTracking.ask_for_new_category()
	elif a == "3":
		newTracking.show_chart()
	elif a == "4":
		newTracking.save_to_disk()
		input("\nDone!\nPress enter to continue")
	elif a == "5":
		newTracking.delete_column()
	elif a == "6":
		while True:
			a = input("\nDo you want to save? y/n ")
			if a == "y":
				newTracking.save_to_disk()
				break
			elif a == "n":
				break

		os.system('cls||clear')
		print("Miss you already!")
		break
	else:
		continue



