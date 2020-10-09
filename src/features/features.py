import pandas as pd
import streamlit as st
from itertools import repeat
import multiprocessing
from multiprocessing import Pool
import pickle
import logging

from src.helper import create_logger

logger = create_logger('Feature', 'logs/Feature.log',
                       logging.DEBUG, logging.WARNING)


class Feature():
    def __init__(self, name, requires=[]):
        self.name = name
        self.requires = requires

    def indicator(self,*args):
        return 0

    def worker(self, tick):
        # fetch childrens
        loc = self.parent.fetch_child_by_name(tick)
        child = self.parent.children[loc[0]]

        # fetch required data
        data = child.data[self.requires]

        # apply Indicator
        new_feature = self.indicator(data)
        logger.debug(f"Work {tick}")
        return [tick, new_feature]

    def apply(self, parent=None):
        if parent:
            self.parent = parent
        # children.add
        if self.name in self.parent.get_feature_list():
            logger.warning(
                "No Update Happened. Try Removing the feature or change the name")
            st.write(f"Feature '{self.name}' Already Exist")
            return False
        try:
            multiprocessing.set_start_method('forkserver')
        except:
            logger.warning("Multiprocessing: context has already been set")

        try:
            logger.info("Started Multiprocessing of creating indicator")
            pool = Pool()
            results = pool.map(self.worker, list(self.parent.ticker_list))
            pool.close()
            pool.join()
            logger.info("Started Adding data into Children")
            for i in results:
                [tick, new_feature] = i
                loc = self.parent.fetch_child_by_name(tick)
                child = self.parent.children[loc[0]]

                child.add_feature(new_feature)
            return self.parent
        except:
            logger.exception("Error in Feature/appy")
            return False

    def register(self):
        self.dump("data/features/" + self.name+".pkl")

    def dump(self, location):
        try:
            with open(location, 'wb') as f:
                pickle.dump(self, f)
        except:
            st.error("Error in dumping Feature File")

    @classmethod
    def load(cls, location):
        try:
            with open(location, 'rb') as f:
                return pickle.load(f), True
        except:
            return None, False
