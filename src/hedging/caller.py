import pandas as pd
import streamlit as st
from multiprocessing import Pool
import logging
import yfinance as yf
from src.helper import create_logger, dump_file
from src.hedging.division import Division

import datetime

logger = create_logger('Caller','logs/Hedging.log', logging.DEBUG, logging.WARNING)

class Caller(Division):
    def __init__(self,govt,location):
        self.gov = govt
        self.loc = location
        self.parent = self.gov.population[self.loc[0]]
        self.market_pulled = False

    def call_parent(self):
        return self.parent

    def pull_childs_in_range(self,start=datetime.datetime(2019,1,1),end=datetime.datetime(2019,1,31)):
        logger.info("Pulling All childrens")
        try:
            return self.parent.fetch_all_child_in_range(start,end)
        except:
            return None

    def pull_market(self):
        new = self.parent.start_date-datetime.timedelta(days = 100)
        self.market = yf.download('^GSPC', start=new, end=self.parent.end_date)
        self.market_pulled = True
        dump_file("data/index_csv/market.pkl",self.market)
        return self.market

    def stat(self):
        dic = {"Market Pulled":self.market_pulled}
        return dic



