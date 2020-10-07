"""Home page shown when the user enters the application"""
import streamlit as st
import logging
import awesome_streamlit as ast
from datetime import datetime
import os
from src.eda.government import Government
from src.helper import create_logger
from src.features.features import Feature
from src.features.indicators.custom_indicator import Custom_indicator

logger = create_logger('viz','logs/Viz.log', logging.DEBUG, logging.WARNING)


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


# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading Playground ..."):
        def update(parent,gov):
            gov.population[loc[0]] = parent
            gov.dump("data/User1.pkl")

        st.write(f"# Get Set Hedge Data playground")
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

        #Turn this off if you want temp files
        parent.clear_dir()

        flag = parent.populate()
        if flag:
            update(parent,gov)

        st.write(parent.get_stats())

        def create_checkbox(name,code,*args,**kwargs):
            agree = st.checkbox(name)
            if agree:
                return code(*args,**kwargs)

        #Check Dataset
        def code1(*args,**kwargs):
            stock = st.selectbox("Select Ticker",parent.everyone_names())
            stock_loc = parent.fetch_child_by_name(stock)
            if len(stock_loc)!=1:
                st.error(f"Issue while finding ticker {stock}")
            else:
                child = parent.children[stock_loc[0]]
            st.write(child.data)
        create_checkbox("Check Dataset",code1,gov,parent,loc)

        #CB2
        create_checkbox("Plot Multiple Tickers into One Graph",gov.plot_multiple_tickers,parent)


        #CB3
        c = Custom_indicator(name="Custom",parent = gov.population[loc[0]])
        c = Custom_indicator(name="ABC",parent = gov.population[loc[0]])
        def code2(gov,parent):
            i_names = os.listdir("data/features/")
            indicator = st.multiselect("Indicators",i_names)
            if st.button("Add Feature(s)"):
                for i in indicator:
                    caller,flag = Feature.load("data/features/"+i)
                    if not flag:
                        st.error("Could Not found indicator. Please Register it separately.")
                    else:
                        with st.spinner("Adding Features..."):
                            new_parent = caller.apply(parent)
                        try:
                            if new_parent==False: #Something wrong happened on backend
                                new_parent = parent
                        except:
                            parent=new_parent
                    update(parent,gov)
                logger.info("Added Features")
                st.write("Added Features. Please Refresh to see updates.")
            return
        create_checkbox("Add Features",code2,gov,parent)


        #CB4
        def code3(gov,parent):
            i_names = parent.get_feature_list()
            remove_features = st.multiselect("Remove Features",i_names)
            if st.button("Delete"):
                with st.spinner("Deleting Features"):
                    parent.remove_features(remove_features)
                    update(parent,gov)
            return
        create_checkbox("Remove Features",code3,gov,parent)

        st.button("Refresh")




