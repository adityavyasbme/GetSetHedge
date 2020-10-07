import pandas as pd
import streamlit as st
from itertools import repeat
import multiprocessing
from multiprocessing import Pool
import pickle
import logging
import time
from src.helper import create_logger

logger = create_logger('Divison','logs/Hedging.log', logging.DEBUG, logging.WARNING)

class Division():
    def pull_range_of_time(self):
        self.range = []
        for x in self.parent.children[0].data.index:
            if x>=self.parent.start_date:
                self.range.append(x)

    def chunks(self,lst, n):
        """Yield successive n-sized chunks from lst."""
        chunk = {}
        counter = 0
        for i in range(0, len(lst), n):
            chunk[counter] = lst[i:i + n]
            counter+=1
        return chunk

    def divide_time(self,rebalancing_freq=25):
        self.pull_range_of_time()
        with st.spinner(f"Found {len(self.range)} rows"):
            self.time_chunks = self.chunks(self.range,rebalancing_freq)

    def stat(self):
        dic = {"time_chunk":{}}
        for key,val in self.time_chunks.items():
            logger.debug("Time Chunk"+str(key)+' has : '+str(len(val))+" " )
            dic["time_chunk"]["chunk"+str(key)]=len(val)
        return dic

