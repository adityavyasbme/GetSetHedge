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
from multiprocessing import Manager
from multiprocessing.sharedctypes import Array
import streamlit as st

logger = create_logger('parent','logs/Parent.log', logging.INFO, logging.WARNING)

class Shops():
    def handle_null():
        pass

    def parser(self,name,ticker):
        if name in listdir(".temp/"):
            try:
                with open(".temp/"+name, 'rb') as f:
                    data= pickle.load(f)
            except:
                pass
        else:
            data = yf.download(ticker, start=self.start_date, end=self.end_date)
            with open(".temp/"+name, 'wb') as f:
                pickle.dump(data, f)
        return data



class Biological_Properties():
    def add_child(self,ticker,data):
        """
        Function to add a ticker object
        """
        try:
            baby = Child(ticker,data)
            #Store the object in population
            logger.debug(f"Storing the baby {ticker}")

            self.children.append(baby)
            return True
        except:
            return False

    def remove_child(self):
        """
        Function to remove the ticker object
        """
        pass
    def everyone(self):
        """
        Function to fetch all the tickers objects
        """
        return self.children

    def everyone_names(self):
        """
        Function to fetch all the names of the ticker objects
        """
        temp= []
        for baby in self.children:
            temp.append(baby.name)
        return temp

    def remove_features(self,names):
        for i in self.children:
            for j in names:
                i.remove_feature(j)




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

    def get_stats(self):
        return {
        "Name":self.name,
        "Number of Tickers":len(self.ticker_list),
        "Current Childrens":len(self.children),
        "Start Date":str(self.start_date),
        "End Date":str(self.end_date)
        }

    def fetch_child_by_name(self,name):
        temp=[]
        logger.debug(f"Fetching child {name}")
        for loc,baby in enumerate(self.children):
            if baby.name==name:
                temp.append(loc)
                logger.debug("found baby")
        return temp

    def get_feature_list(self):
        for i in self.children:
            self.feature_list = i.get_features()
            return self.feature_list




class Parent(Biological_Properties,Secure_Properties,Shops):
    def __init__(self,index_name,ticker_list,start_date,end_date):
        self.name = index_name
        self.ticker_list = ticker_list
        self.children = []
        self.start_date = start_date
        self.end_date = end_date
        self.feature_list = []

    def worker(self,tick):
        name = str(tick)+'_'+str(self.start_date)+"_"+str(self.end_date)+".pkl"
        fetched_data = self.parser(name,tick)
        return [tick,fetched_data]

    def populate(self):
        if len(self.children)==0:
            logger.info("Ticker Addition Process Initiated")
            logger.info(f"Found {len(self.ticker_list)} tickers")
            try:
                multiprocessing.set_start_method('forkserver')
            except:
                logger.warning("Multiprocessing: context has already been set")

            pool=Pool()
            results = pool.map(self.worker, list(self.ticker_list))
            pool.close()
            pool.join()
            for i in results:
                [name,data]=i
                self.add_child(name,data)
            logger.info("Processing Closed")

