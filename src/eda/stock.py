import pandas as pd
import numpy as np 

class Teacher_Knowledge():
	def childanalyzer():
		pass

	def check_feature_length():
		return len(self.data.columns)

class Child_Capabilities():
	def add_feature():
		"""
		Function to append single feature in the dataframe 
		Updates self.data
		"""
		pass

	def remove_feature():
		"""
		Function to remove the feature from a dataframe 
		Updates self.data
		"""
		pass

class Child(Teacher_Knowledge,Child_Capabilities):
	def __init__(self,ticker,start_date,end_date,data:pd.DataFrame):
		self.name = ticker
		self.start_date = start_date
		self.end_date = end_date
		self.data = data
