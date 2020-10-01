#Has function that handles null value

#Has function to check the date range
import logging
from src.eda.parent import Parent
import yfinance as yf
import streamlit as st
import pickle
import numpy
import pandas as pd 
from src.helper import create_logger
from src.eda.graphs import Graph

logger = create_logger('process','logs/Government.log', logging.DEBUG, logging.WARNING)


class Control_Population():
	def add_parent(self,filename,start_date,end_date):
		"""
		Takes in filename, and Fetches all it's tickers
		Filename = default.csv
		"""
		location = 'data/index_csv/'+ filename
		logger.debug(f"Looking for {location}")
		try:
			data = pd.read_csv(location)
			ticker_list = data["Symbol"]
		except:
			logger.error(f"Error in Reading {location} File")
			st.write(f"Error in Reading {location} File")
			return False


		logger.debug(f"Checking population")
		for j in self.fetch_parent_by_nate(filename[:-4],start_date,end_date):
			logger.warning("Found Existing Parent")
			return False

		try:
			parent = Parent(filename[:-4],ticker_list,start_date,end_date)
			self.population.append(parent)
			logger.info("Parent Added")
			return True
		except:
			logger.exception("Error In adding the parent")
			return False
		
	def remove_parent(self,filename,start_date,end_date):
		"""
		Fetches all parent and delete the parent with the filename
		"""
		#Check if Parent Exist
		try:

			logger.info(f"Looking for parent matching the name: {filename} and start_date:{start_date} and end_date: {end_date}")
			for i in self.fetch_parent_by_nate(filename[:-4],start_date,end_date):
				logger.info("Found Parent")
				self.population.pop(loc)
				logger.info(f"Successfully removed {filename} parent")
				return True
		except:
			logger.exception("Error while removing the parent")
			return False

	def fetch_parent_by_name(self,name):
		temp = []
		for loc,parent in enumerate(self.population):
			if parent.name == name:
				temp.append(loc)
		return temp

	def fetch_parent_by_nate(self,name,start_date,end_date): 
		temp = []
		for loc in self.fetch_parent_by_name(name):
			try:
				if self.population[loc].start_date==start_date.date() and self.population[loc].end_date==end_date.date():
					logger.debug("Found Parent")
					temp.append(loc)
			except:
				if self.population[loc].start_date==start_date and self.population[loc].end_date==end_date:
					logger.debug("Found Parent")
					temp.append(loc)
		return temp



class Government_Rules():
	def get_population(self):
		return self.population

	def population_names(self):
		return [parent.name for parent in self.get_population()]

	def set_tracker(self):
		dic = {}
		for loc,parent in enumerate(self.population):
			dic[loc] = f"{parent.name} FROM {str(parent.start_date)} TO {str(parent.end_date)}"

		index = st.selectbox("Select Tracker", list(dic.values()))
		if index:
			st.write(f"Selected Tracker {index}")

		self.track = index

	def get_tracker(self):
		try:
			return self.track
		except:
			logger.exception("Tracker Not Set")

	#Check if all the childs have same set of features
	#Check if all the child have same size
	#Check if specific path exists
	#check if data/index_csv
	#Check .temp/ exist if not then create it
	#Create hyperparameter files


class Government(Control_Population,Government_Rules,Graph):

	def __init__(self,government_name):
		self.government = government_name
		self.population = []
		logger.info("Government Initiated")

	def dump(self,location):
		try:
			with open(location, 'wb') as f:
				pickle.dump(self, f)
		except:
			st.error("Error in dumping File")

	@classmethod
	def load_government(cls,location):
		try:
			with open(location, 'rb') as f:
				return pickle.load(f),True
		except:
			return None,False



