"""The Gallery index page is used to navigate between examples
Very much inspired by:
Author: [Nhan Nguyen](https://github.com/virusvn)
Source: https://github.com/virusvn/streamlit-components-demo/blob/master/app.py
Credits to Nhan for sharing that code
"""
import logging
from typing import List
import streamlit as st
import awesome_streamlit as ast
import datetime
from src.eda.government import Government
from src.helper import find_csv_filenames, read_csv

logger = logging.getLogger('input')

def write():
    """This method writes the Gallery index page which is used to navigate between gallery apps"""
    ast.shared.components.title_awesome("Select Index Name")

    start_date = st.sidebar.date_input('start date', datetime.date(2019,1,1))
    end_date = st.sidebar.date_input('End date', datetime.date(2019,3,31))


    #TODO: fill up the index_list
    index_list = find_csv_filenames("data/index_csv")
    index = st.selectbox("Select Index Name", index_list)
    if not index:
        st.error('Please update input so that blah, blah...')
        st.stop()

    gov,flag = Government.load_government("data/User1.pkl")
    if not flag:
        gov = Government("User1")
        gov.add_parent(index,start_date,end_date)

    if st.button('Add Tracker Config'):
        gov.add_parent(index,start_date,end_date)
        gov.dump("data/User1.pkl")

    cb1 = st.checkbox('Available Trackers')
    if cb1:
        st.write([i.get_stats() for i in gov.get_population()])

    cb2 = st.checkbox('Set Tracker')
    if not cb2:
        st.stop()
    else:
        gov.set_tracker()

    gov.dump("data/User1.pkl")





if __name__ == "__main__":
    write()
