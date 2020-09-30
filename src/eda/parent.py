# Contains list stock objects (add/delete/remove/update)
import datetime

class Shops():
	def handle_null():
		pass

class Biological_Properties():
	def add_child(self):
		"""
		Function to add a ticker object
		"""
		pass
	def remove_child(self):
		"""
		Function to remove the ticker object
		"""
		pass
	def everyone(self):
		"""
		Function to fetch all the tickers objects
		"""
		pass
	def everyone_names(self):
		"""
		Function to fetch all the names of the ticker objects
		"""
		pass

class Secure_Properties():
	def refractor():
		"""
		Function to check if all the stock objects has same number of rows for processing
		Check for inconsitencies
		"""
		pass

	def check_feature_consistency(self,population):
		temp=[]
		for i in population:
			temp.append(i.check_feature_length())
		if len(np.unique(temp))==1:
			return True
		return False


class Parent(Biological_Properties,Secure_Properties):
	def __init__(self,index_name,ticker_list,start_date,end_date):
		self.name = index_name
		self.ticker_list = ticker_list
		self.children = []
		self.start_date = start_date
		self.end_date = end_date

	def add_children():
		logger.info("Ticker Addition Process Initiated")
		logger.info(f"Found {len(self.ticker_list)} tickers")

		for tick in self.ticker_list:
			logger.info("-------------------------------------------")
			
			#Fetch Data
			logger.info(f"Fetching Data")
			fetch_data = self.download_data(tick)

			#Create a child object
			logger.info(f"Creating child:{tick}")
			baby = self.create_child(tick,fetch_data)

			#Check for inconsitency
			logger.info(f"Handling Data")

			#Store the object in population
			logger.info("Storing the data")
			self.population.append(baby)

			logger.info("-------------------------------------------")
		logger.info("Processing Closed")

		self.dump(f"data/{self.index}.pkl")

	def get_stats(self):
		return {
		"Name":self.name,
		"Number of Tickers":len(self.ticker_list),
		"Current Childrens":len(self.children),
		"Start Date":str(self.start_date),
		"End Date":str(self.end_date)
		}




