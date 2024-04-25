import pandas as pd 
import os
from pprint import pprint
import time
import datetime
#import plotly


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
		while True:
			try:
				lastDate = self.DF["Date"].to_list()[-1]
				if self.today == lastDate:
					break
				else:
					self.DF = self.DF.append({"Date": self.add_day(lastDate)}, ignore_index=True)
			except:
				print("First entry or error")
				self.DF = self.DF.append({"Date": self.today}, ignore_index=True)

			
		#Set the today index
		self.todayIndex = self.DF.index[-1]


	def add_day(self, date):
		datetime_object = datetime.datetime.strptime(str(date), "%Y-%m-%d")
		tomorrow = datetime_object + datetime.timedelta(days=1)
		return str(tomorrow.date())

	def save_to_disk(self):
		self.DF.to_csv(self.path, index=False)

	def print_date(self):
		pass

	def print_columns(self):
		i = 1
		catList = self.DF.columns.to_list()
		if len(catList) > 1:
			for i in range(1, len(catList)):
				print(str(i)+":", catList[i])
		else:
			print("There is no category yet :( \n")

	def add_data(self, columns_index, value, index=None):
		#Get column name base on index
		columnName = self.DF.columns.to_list()[columns_index]

		#If index is default then set to today
		#Later useful to change the past
		if index == None:
			#Change a single value
			self.DF[columnName][self.todayIndex] = value		
		else:
			self.DF[columnName][index] = value


	def choose_date(self):
		os.system('cls||clear')

		dateList = self.DF.tail(7)["Date"].to_list()
		dateList.reverse()
		for i in range(len(dateList)):
			print(str(i)+":", dateList[i])

		while True:
			try:
				choice = input("\nChose a date(Default is today): ")

				if choice == "":
					return len(dateList) - 1
				else:
					return len(dateList) - int(choice) - 1
			except:
				os.system('cls||clear')
				input("Enter only numbers please. Press enter to continue")
				os.system('cls||clear')


	def ask_for_new_data(self):
		categoryList = list(self.DF.columns)

		# if there is more then Date category
		if len(categoryList) > 1:

			index = self.choose_date()

			os.system('cls||clear')
		
			self.print_columns()
			columns_index = int(input("Which category you want to update?"))
			os.system('cls||clear')
			value = input("What do you want to say for {}?\n".format(self.DF.columns.to_list()[columns_index]))
			self.add_data(columns_index, value, index=index)
		else:
			#No category to add date
			print("There is no category")
			input("\nPress enter to continue")


	def ask_for_new_category(self):
		os.system('cls||clear')
		
		print("Current category:")
		self.print_columns()

		category = input("Name your new category: \n")

		#Dict = {key: [type, exemple]}
		catDict = {	1: ["yes/no"],
					2: ["#", "ex: minute that you run that day"],
					3: ["range", "ex: happyness level 0 to 100"],
					4: ["note", "just text"]
		}
		print("\n")
		for k, v in catDict.items():
			print("{}: {}".format(k,v))

		#Ask which category
		categoryType = int(input("\nChoose category type for {}? ".format(category)))
		# if choose range
		# else just put the dict[key][0]
		if categoryType == 3:
			r = input("Range will be from 0 to ?: \n")
			categoryName = "{}(0-{})".format(category, r)
		else:
			categoryName = "{}({})".format(category, catDict[categoryType][0])

		#Create the new empty category 
		self.DF[categoryName] = ""

	def delete_column(self):
		self.print_columns()
		columns_index = int(input("\nWhich columns you want to delete?"))
		columnName = self.DF.columns.to_list()[columns_index]
		self.DF.drop(columns=columnName, inplace=True)

	def show_chart(self, category=None):
		os.system('cls||clear')
		if category == None:
			print(self.DF)
		else:
			print(self.DF[["Date", category]])
		input("\nPress enter to continue")


'''
Track your life
'''
newTracking = Tracking()
x=newTracking


optionDict = {	1:"Add new data",
				2:"Add new category",
				3:"Show everything",
				4:"Show one category",
				5:"Delete one category",
				6:"Save",
				7:"Quit",
				8:"Graph"
}

while True:
	os.system('cls||clear')
	for k, v in optionDict.items():
		print("{}: {}".format(k,v))

	#Ask for option
	a = input("Choose one option: ")

	if a == "1":
		newTracking.ask_for_new_data()
	elif a == "2":
		newTracking.ask_for_new_category()
	elif a == "3":
		newTracking.show_chart()
	elif a == "4":
		os.system('cls||clear')
		newTracking.print_columns()
		columns_index = int(input("\nChoose a category: "))
		columnName = newTracking.DF.columns.to_list()[columns_index]
		newTracking.show_chart(columnName)
	elif a == "5":
		newTracking.delete_column()
	elif a == "6":
		newTracking.save_to_disk()
		input("\nDone!\nPress enter to continue")
	elif a == "7":
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
	elif a == "8":
		pass
	else:
		continue


