"""Home page shown when the user enters the application"""
import streamlit as st
import logging
import awesome_streamlit as ast
from datetime import datetime

from src.eda.government import Government
from src.helper import create_logger

logger = create_logger('viz','logs/Viz.log', logging.DEBUG, logging.WARNING)

# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading About ..."):

        st.write(
        f"# GetSetHedge Data playground")

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

        parent = gov.population[loc[0]]
        st.write(parent.get_stats())

        cb1 = st.checkbox("Populate")
        if cb1:
        	# parent.populate()
        	pass


        st.markdown("""**Data Page**""",unsafe_allow_html=True)
        st.stop()

