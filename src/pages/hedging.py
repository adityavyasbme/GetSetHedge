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

import statsmodels.api as sm

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


def hedge(call,n,class_name): #n represents number of ticker in a decile
    portfolio = pd.DataFrame()
    with st.spinner(f"Buying/Selling Stocks based on {class_name.__name__}. Please Wait... It might take long"):
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
                        logger.warning(f"Date Not Found : {date}. The data is {call.parent.children[loc[0]].name}")
                        val = 0
                    upper_decile[i] *= (val/stock_in_decile)

                for i in lower_decile.index:
                    loc = call.parent.fetch_child_by_name(i)
                    try:
                        val = call.parent.children[loc[0]].data["Adj Close"][date]
                    except:
                        logger.warning(f"Date Not Found : {date}. The data is {call.parent.children[loc[0]].name}")
                        val = 0
                    lower_decile[i] *= (val/stock_in_decile)

                factor = sum(upper_decile) - sum(lower_decile)
                portfolio = portfolio.append({"Date":date,f"Bab@t{chunk_num}":factor},ignore_index=True)

        portfolio = portfolio.set_index("Date")
        # st.write(portfolio)
        maxValuesObj = portfolio.max(axis=1)
        maxValuesObj = maxValuesObj.rename("BAB")
        return maxValuesObj


def hedge_dataframe(call,class_name,n):
    with st.spinner(f"Working on {class_name.__name__}"):

        portfolio = pd.DataFrame()
        #pull in data for all child
        data = pd.DataFrame()
        for baby in call.parent.children:
            tick= class_name(baby).calculate(call.parent.start_date)
            data = data.append(tick)
        # st.write(data)
        data = data.dropna(how='all')
        for date in data.columns: #For Each date in data.columns
            if data[date].isnull().all():
                portfolio = portfolio.append({"Date":date,f"BaM":0},ignore_index=True)
                continue

            data = data.sort_values(by=[date],ascending=False)

            upper_decile = data[date].head(n).copy()
            lower_decile = data[date].tail(n).copy()

            stock_in_decile = len(upper_decile)

            for i in upper_decile.index:
                loc = call.parent.fetch_child_by_name(i)
                try:
                    val = call.parent.children[loc[0]].data["Adj Close"][date]
                except:
                    logger.warning(f"Date Not Found : {date}. The data is {call.parent.children[loc[0]].name}")
                    val = 0
                upper_decile[i] *= (val/stock_in_decile)

            for i in lower_decile.index:
                loc = call.parent.fetch_child_by_name(i)
                try:
                    val = call.parent.children[loc[0]].data["Adj Close"][date]
                except:
                    logger.warning(f"Date Not Found : {date}. The data is {call.parent.children[loc[0]].name}")
                    val = 0
                lower_decile[i] *= (val/stock_in_decile)

            factor = sum(upper_decile) - sum(lower_decile)
            portfolio = portfolio.append({"Date":date,f"BaM":factor},ignore_index=True)

        portfolio = portfolio.set_index("Date")
        # st.write(portfolio)

        maxValuesObj = portfolio.max(axis=1)
        maxValuesObj = maxValuesObj.rename("BAM")
        return maxValuesObj



# pylint: disable=line-too-long
def write():
    def update(parent,gov):
        gov.population[loc[0]] = parent
        gov.dump("data/User1.pkl")

    def create_checkbox(name,code,*args,**kwargs):
        agree = st.checkbox(name)
        if agree:
            return code(*args,**kwargs)

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

        bab = False
        bam = False
        if bab:
            #Create Factors
            call = Caller(govt=gov,location=loc)
            call.divide_time()
            call.pull_market()
            parent.Factors["BAB"]=hedge(call,2,Beta)
            update(parent,gov)

        if bam:
            call = Caller(govt=gov,location=loc)
            parent.Factors["BAM"] = hedge_dataframe(call,Momentum,2)
            update(parent,gov)

        result = pd.concat(parent.Factors.values(),axis=1)
        st.write(result)

        def final_regression(name="AAPL"):
            child_loc = parent.fetch_child_by_name(name)
            child = parent.children[child_loc[0]]
            if not child:
                st.error("Child Not found")
            y = child.data["Adj Close"]
            mask =  (y.index >= min(result.index)) & (y.index <= max(result.index))
            y = y[mask]

            model = sm.OLS(y, result[['BAB','BAM']])

            # fit model and print results
            regression = model.fit()
            for i in parent.Factors.keys():
                st.write(f"{name} is exposed to {i} by {float(regression.params[i]*100)} %")

        create_checkbox("Apply Regression",final_regression)







