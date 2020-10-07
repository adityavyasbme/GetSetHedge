import streamlit as st
import logging
import awesome_streamlit as ast
from datetime import datetime
import os
from src.eda.government import Government
from src.helper import create_logger
from multiprocessing import Pool

logger = create_logger('Hedging_Page','logs/Hedging.log', logging.DEBUG, logging.WARNING)
from src.hedging.caller import Caller
from src.hedging.parser import Parser
from src.hedging.factors.beta import Beta
from src.hedging.factors.momentum import Momentum

import pandas as pd
import numpy as np

def fetch_tracker(tracker,gov):
    #Fetch the tracker and find it's location
    tracker = tracker.split()
    name = tracker[0]
    logger.debug({"Tracking Index":name})
    start_date=datetime.strptime(tracker[2],'%Y-%m-%d')
    logger.debug({"Start Date":start_date})
    end_date=datetime.strptime(tracker[4],'%Y-%m-%d')
    logger.debug({"End Date":end_date})
    loc = gov.fetch_parent_by_nate(name,start_date,end_date)
    if len(loc)!=1:
        st.error("Issue while setting tracker")
        st.stop()
    return loc


def hedge(call,n,class_name):
    portfolio = pd.DataFrame()
    with st.spinner("Buying/Selling Stocks based on Factor. Please Wait... It might take long"):
        for chunk_num in range(len(call.time_chunks)): #For a specific time Frame
            parser = Parser(call) #create a parser object

            with st.spinner(f"Working on Time Frame {chunk_num}"):
                data = parser.parse_multiple(chunk_num,class_name) #Fetch data for specific time frame

            for date in data.columns: #For Each date in data.columns
                data = data.sort_values(by=[date],ascending=False)
                upper_decile = data[date].head(n).copy()
                lower_decile = data[date].tail(n).copy()

                stock_in_decile = len(upper_decile)
                for i in upper_decile.index:
                    loc = call.parent.fetch_child_by_name(i)
                    try:
                        val = call.parent.children[loc[0]].data["Adj Close"][date]
                    except:
                        st.error(f"Date Not Found : {date}. The data is {call.parent.children[loc[0]].name}")
                        val = 0
                    upper_decile[i] *= (val/stock_in_decile)

                for i in lower_decile.index:
                    loc = call.parent.fetch_child_by_name(i)
                    try:
                        val = call.parent.children[loc[0]].data["Adj Close"][date]
                    except:
                        st.error(f"Date Not Found : {date}. The data is {call.parent.children[loc[0]].name}")
                        val = 0
                    lower_decile[i] *= (val/stock_in_decile)

                factor = sum(upper_decile) - sum(lower_decile)
                portfolio = portfolio.append({"Date":date,f"Bab@t{chunk_num}":factor},ignore_index=True)

        portfolio = portfolio.set_index("Date")
        # st.write(portfolio)
        maxValuesObj = portfolio.max(axis=1)
        maxValuesObj = maxValuesObj.rename("BAB")
        return maxValuesObj


# pylint: disable=line-too-long
def write():
    def update(parent,gov):
        gov.population[loc[0]] = parent
        gov.dump("data/User1.pkl")

    """Used to write the page in the app.py file"""
    with st.spinner(""):
        logger.info("Hedging Page Opened")
        st.write(
        f"# Factor Construction")

        def checks():
            global tracker, gov
            #The pkl file should be there for a particular user
            logger.info("Finding Government")
            gov,flag = Government.load_government("data/User1.pkl")
            if not flag:
                st.error("User Profile Not Found. Go to Input")
                logger.warning("User Profile not found.")
                st.stop()

            #The tracker should be set
            logger.info("Checking if tracker is set or not")
            tracker = gov.get_tracker()
            if not tracker:
                st.error("Tracker Not set. Go to Input")
                logger.warning("Tracker Not found.")
                st.stop()

        checks()
        loc=fetch_tracker(tracker,gov)
        parent = gov.population[loc[0]]

        if len(parent.Factors)==0:
            #Create Factors
            call = Caller(govt=gov,location=loc)
            call.divide_time()
            call.pull_market()
            parent.Factors.append(hedge(call,2,Beta))
            update(parent,gov)
        else:
            for factors in parent.Factors:
                st.write(factors)


        # call.parent.clear_dir()








