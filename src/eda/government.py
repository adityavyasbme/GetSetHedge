"""This script contains code for the Goverment class and it's inherited properties
"""
import logging
from src.eda.parent import Parent
import streamlit as st
import pickle
import pandas as pd
from src.helper import create_logger
from src.eda.graphs import Graph


logger = create_logger('process', 'logs/Government.log',
                       logging.DEBUG, logging.WARNING)


class Control_Population():
    """Perform CRUD operations.
    """

    def __init__(self):
        self.population = {}

    def add_parent(self, filename, start_date, end_date):
        """Adds Parent into Government controlled Population.

        Args:
            filename (str): name of Parent(Ticker Symbol)
            start_date (date): Start date
            end_date (date): [description]

        Returns:
            True -> Success
            False -> Failure
        """
        location = 'data/index_csv/' + filename
        logger.debug(f"Looking for {location}")
        try:
            data = pd.read_csv(location)
            ticker_list = data["Symbol"]
        except:
            logger.error(f"Error in Reading {location} File")
            st.write(f"Error in Reading {location} File")
            return False

        logger.debug("Checking population")
        for j in self.fetch_parent_by_nate(filename[:-4], start_date, end_date):
            logger.warning(f"Found Existing Parent location: {j}")
            return False

        try:
            parent = Parent(filename[:-4], ticker_list, start_date, end_date)
            self.population.append(parent)
            logger.info("Parent Added")
            return True
        except:
            logger.exception("Error In adding the parent")
            return False

    def remove_parent(self, filename, start_date, end_date):
        """Remove parent from Government controlled Population.

        Args:
            filename (str): name of Parent(Ticker Symbol)
            start_date (date): Start date
            end_date (date): End date

        Returns:
            True -> Success
            False -> Failure
        """
        # Check if Parent Exist
        try:

            logger.info(
                f"Looking for parent matching the name: {filename} and start_date:{start_date} and end_date: {end_date}")
            for i in self.fetch_parent_by_nate(filename[:-4], start_date, end_date):
                logger.info("Found Parent")
                self.population.pop(i)
                logger.info(f"Successfully removed {filename} parent")
                return True
        except:
            logger.exception("Error while removing the parent")
            return False

    def fetch_parent_by_name(self, name):
        """Search Parent by name

        Args:
            name (str): name of parent (Ticker name)

        Returns:
            List of Parent Object
        """
        temp = []
        for loc, parent in enumerate(self.population):
            if parent.name == name:
                temp.append(loc)
        return temp

    def fetch_parent_by_nate(self, name, start_date, end_date):
        """Search Parent by name as well as date

        Args:
            name (str): name of parent (Ticker name)
            start_date (date): Start date
            end_date (date): End date

        Returns:
            List of Parent Object
        """

        temp = []
        for loc in self.fetch_parent_by_name(name):
            try:
                if self.population[loc].start_date == start_date.date() and self.population[loc].end_date == end_date.date():
                    logger.debug("Found Parent")
                    temp.append(loc)
            except:
                if self.population[loc].start_date == start_date and self.population[loc].end_date == end_date:
                    logger.debug("Found Parent")
                    temp.append(loc)
        return temp


class Government_Rules():
    """This is a Tracker class
    """

    def __init__(self):
        self.population = {}

    def get_population(self):
        """
        Returns:
            return all the population
        """
        return self.population

    def population_names(self):
        """
        Returns:
            return names of all the population
        """
        return [parent.name for parent in self.get_population()]

    def set_tracker(self):
        """
        Description:
            Sets the tracker which the framework will point to.
        """

        dic = {}
        for loc, parent in enumerate(self.population):
            dic[loc] = f"{parent.name} FROM {str(parent.start_date)} TO {str(parent.end_date)}"

        index = st.selectbox("Select Tracker", list(dic.values()))
        if index:
            st.write(f"Selected Tracker {index}")

        self.track = index

    def get_tracker(self):
        """
        Returns:
            Gets the tracker which the framework is pointing to.
        """
        try:
            return self.track
        except:
            logger.exception("Tracker Not Set")

    # Check if all the childs have same set of features
    # Check if all the child have same size
    # Check if specific path exists
    # check if data/index_csv
    # Check .temp/ exist if not then create it
    # Create hyperparameter files


class Government(Control_Population, Government_Rules, Graph):
    """Government Class

    Args:
        Control_Population (class): CRUD Parents
        Government_Rules (class): Tracker class
        Graph ([class]): Graph class for visualization
    """

    def __init__(self, government_name):
        """Inititates Government.

        Args:
            government_name (str): Name of the government
        """
        self.government = government_name
        self.population = []
        logger.info("Government Initiated")

    def dump(self, location: str):
        """Dumps the government object into a pickle file to a desired location.

        Args:
            location (str): Name of Location.
        """
        try:
            with open(location, 'wb') as f:
                pickle.dump(self, f)
        except:
            st.error("Error in dumping File")

    @classmethod
    def load_government(cls, location: str):
        """Loads the government object from a pickle file save into a specified location.

        Args:
            location (str): Location of file.

        Returns:
            File -> None if file not found
            Flag -> Error Happened/File not found.
        """

        try:
            with open(location, 'rb') as f:
                return pickle.load(f), True
        except:
            return None, False
