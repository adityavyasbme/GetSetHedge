# Contains list stock objects (add/delete/remove/update)
import datetime
from src.helper import create_logger
from src.eda.child import Child
import yfinance as yf
from os import listdir
import pickle
import logging
import os
import multiprocessing
from multiprocessing import Pool
import shutil
import numpy as np

logger = create_logger('parent', 'logs/Parent.log',
                       logging.INFO, logging.WARNING)


class Shops():
    """Data Source
    """

    def __init__(self):
        self.start_date = None
        self.end_date = None

    def parser(self, name, ticker):
        """
        Description:
            Function to take name and ticker and download data from yfinance
        Args:
            name (str) : Name of the file to store in temp folder
            ticker (str) : Ticker Symbol
        """
        if name in listdir(".temp/"):
            try:
                with open(".temp/"+name, 'rb') as f:
                    data = pickle.load(f)
            except:
                pass
        else:
            self.new_date = self.start_date-datetime.timedelta(days=100)
            data = yf.download(ticker, start=self.new_date, end=self.end_date)
            with open(".temp/"+name, 'wb') as f:
                pickle.dump(data, f)
        return data


class Biological_Properties():
    """CRUD Child
    """

    def __init__(self):
        self.children = []

    def add_child(self, ticker, data):
        """
        Description:
            Function to add a ticker object
        """
        try:
            baby = Child(ticker, data)
            # Store the object in population
            logger.debug(f"Storing the baby {ticker}")

            self.children.append(baby)
            return True
        except:
            return False

    def remove_child(self):
        """
        TODO: Function to remove the ticker object
        """
        pass

    def everyone(self):
        """
        Description:
            Function to fetch all the tickers objects
        """
        return self.children

    def everyone_names(self):
        """
        Description:
            Function to fetch all the names of the ticker objects
        """
        temp = []
        for baby in self.children:
            temp.append(baby.name)
        return temp

    def remove_features(self, names):
        """
        Args:
            names (str): Name of the Feature
        """
        for i in self.children:
            for j in names:
                i.remove_feature(j)


class Secure_Properties():
    """Tracker Based Class
    """

    def __init__(self):
        self.children = []
        self.name = None
        self.ticker_list = []
        self.start_date = None
        self.end_date = None

    def refractor(self):
        """
        Function to check if all the stock objects has same number of rows for processing
        Check for inconsitencies
        """
        pass

    def check_feature_consistency(self, population):
        """Check if all the childs have same number of feature length

        Args:
            population : List storing all the childrens

        Returns:
            Boolean
        """
        temp = []
        for i in population:
            temp.append(i.check_feature_length())
        if len(np.unique(temp)) == 1:
            return True
        return False

    def get_stats(self):
        """return basic information about parent

        Returns:
            dictionary
        """
        return {
            "Name": self.name,
            "Number of Tickers": len(self.ticker_list),
            "Current Childrens": len(self.children),
            "Start Date": str(self.start_date),
            "End Date": str(self.end_date)
        }

    def fetch_child_by_name(self, name):
        """Search child by name

        Args:
            name (str): Name of child (Ticker)

        Returns:
            List of child objects
        """
        temp = []
        logger.debug(f"Fetching child {name}")
        for loc, baby in enumerate(self.children):
            if baby.name == name:
                temp.append(loc)
                logger.debug("found baby")
        return temp

    def fetch_data_in_range(self, baby, start_date, end_date):
        """Fetch data by the date range

        Args:
            baby (object): Child Object
            start_date (Date): start date
            end_date (Date) : end date

        Returns:
            pd.DataFrame
        """
        logger.info(f"Fetching children: {baby.name}")
        data = baby.data.copy()
        data.reset_index(inplace=True)
        data = data.rename(columns={'index': 'Date'})

        try:
            mask = (data['Date'] > start_date) & (data['Date'] <= end_date)
        except:
            logger.warning(
                "Error in Creating Mask of a children. Check code in Parent.py")
        data = data.loc[mask]
        return data

    def fetch_all_child_in_range(self, start_date, end_date):
        """Fetch all childs in a certain date range

        Args:
            start_date (Date): start date
            end_date (Date) : end date

        Returns:
            pd.DataFrame
        """
        temp = {}
        logger.info(f"Fetching All Childs from {start_date} to {end_date}")
        logger.info(f"Children Size {len(self.children)}")
        for _, baby in enumerate(self.children):
            data = self.fetch_data_in_range(baby, start_date, end_date)
            temp[baby.name] = data
        return temp

    def get_feature_list(self):
        """
        Returns:
            Names of all the feature present in the child data
        """
        for i in self.children:
            self.feature_list = i.get_features()
            return self.feature_list

    def clear_dir(self, path_=".temp/"):
        """
        Function to clear a directory

        Args:
            path_ (str, optional): Defaults to ".temp/".
        """
        try:
            shutil.rmtree(path_)
            os.mkdir(path_)
        except:
            os.mkdir(path_)


class Parent(Biological_Properties, Secure_Properties, Shops):
    """Parent Class.

    Args:
        Biological_Properties: CRUD childs (Stocks)
        Secure_Properties : Tracker based properties
        Shops : Class to pull in Data
    """

    def __init__(self, index_name: str, ticker_list, start_date, end_date):
        """
        Args:
            index_name (str): Name of the Parent (Index Name)
            ticker_list (List): List of Ticker Symbols
            start_date (Date): Date object
            end_date (Date): Date object
        """

        self.name = index_name
        self.ticker_list = ticker_list
        self.children = []  # Stores individual stocks
        self.start_date = start_date
        self.end_date = end_date
        self.feature_list = []  # Stores feature present in the data
        self.Factors = {}  # Stores associated factors

    def worker(self, tick):
        """
        Worker that pulls in data from Shop
        Args:
            tick (str): Name of the ticker

        Returns:
            Ticker name,Ticker Data
        """
        name = str(tick)+'_'+str(self.start_date)+"_"+str(self.end_date)+".pkl"
        fetched_data = self.parser(name, tick)
        return [tick, fetched_data]

    def populate(self):
        """Assign job to worker and populate Childs (Stock Data)

        Returns:
            Boolean
        """
        if len(self.children) == 0:
            logger.info("Ticker Addition Process Initiated")
            logger.info(f"Found {len(self.ticker_list)} tickers")
            try:
                multiprocessing.set_start_method('forkserver')
            except:
                logger.warning("Multiprocessing: context has already been set")

            pool = Pool()
            results = pool.map(self.worker, list(self.ticker_list))
            pool.close()
            pool.join()
            for i in results:
                [name, data] = i
                self.add_child(name, data)
            logger.info("Processing Closed")
            return True
        return False
