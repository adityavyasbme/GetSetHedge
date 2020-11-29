import pandas as pd
import logging
from src.helper import create_logger

logger = create_logger('child', 'logs/Child.log',
                       logging.DEBUG, logging.WARNING)


class Teacher_Knowledge:
    """Tracker Based Class
    """
    def __init__(self):
        self.data = None

    def childanalyzer(self):
        """
        TODO: Some kind of data Analyzer
        """
        pass

    def get_features(self):
        """
        Returns:
            Name of Features
        """
        return self.data.columns

    def check_feature_length(self):
        """
        Returns:
            Length of Features
        """
        return len(self.data.columns)


class Child_Capabilities:
    def add_feature(self, new_feature: pd.DataFrame):
        """
        Function to append single feature in the dataframe
        Updates self.data
        """
        logger.debug(
            "-------------------------------------------------------------")
        logger.info(f"Column Names: {new_feature.columns}")
        new_feature_list = new_feature.columns
        common_elements = list(
            set(new_feature_list).intersection(set(self.data.columns)))

        for i in common_elements:
            try:
                new_feature = new_feature.drop(i, axis=1)
            except:
                logger.warning(f"Column: {i} Not Found")
        if len(new_feature) == len(self.data):
            self.data = pd.concat([self.data, new_feature], axis=1)
        else:
            logger.warning(
                f"Length of new_features: {len(new_feature)} and current data: {len(self.data)} is not same")

    def remove_feature(self, name):
        """
        Function to remove the feature from a dataframe
        Updates self.data
        """
        try:
            self.data = self.data.drop(name, axis=1)
        except:
            logger.warning("Column Not Found")


class Child(Teacher_Knowledge, Child_Capabilities):
    """Child(Stock) Class

    Args:
        Teacher_Knowledge : Tracker based class
        Child_Capabilities : CRUD Features
    """
    def __init__(self, ticker, data):
        self.name = ticker
        self.data = data
