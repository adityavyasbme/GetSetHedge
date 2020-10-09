import pandas as pd
import streamlit as st
from multiprocessing import Pool
import logging
import yfinance as yf
from src.helper import create_logger
from src.hedging.division import Division
import datetime

import importlib
import inspect
import os
import glob
import itertools
from glob import iglob
from os.path import basename, relpath, sep, splitext
logger = create_logger('Parser', 'logs/Hedging.log',
                       logging.DEBUG, logging.WARNING)


class Parser():
    def __init__(self, caller):
        self.factor = []
        self.call = caller

    def import_plugins(self, *args, **kwargs):
        return 0

    # def find_all_factor(self):
    #     # Find factors in factors folder and their requirement
    #     # lis = os.listdir("src/hedging/factors/")
    #     self.factors = self.import_plugins(
    #         "src/hedging/factors/", create_instance=False, filter_abstract=False)
    #     return self.factors
    #     # a = self.import_submodules("src/hedging/factors/")

    def run_factor(self, class_name, baby, time_chunk):

        obj = class_name(baby, market_name="^GSPC")
        pool = Pool()
        try:
            results = pool.map(obj.calculate, list(time_chunk))
        except:
            pool.close()
            return pd.DataFrame()
        pool.close()
        pool.join()
        df = pd.DataFrame()
        for i in results:
            df = df.append(i, ignore_index=True)
        df = df.set_index("Date")

        # for x in time_chunk:
        #     beta = factor.calculate(baby,x,self.pull_yahoo_API,stat=False)
        #     data = data.append({"Date":x,baby.name:beta},ignore_index=True)
        #     break
        # data = data.set_index("Date")
        # st.write(df)

        return df.T

    def parse_multiple(self, num, class_name):
        # list of all children
        # get chunk of data where time_chunk
        time_chunk = self.call.time_chunks[num]
        c = pd.DataFrame()
        for baby in self.call.parent.children:
            # For multiple babies
            logging.info(f"Running for {baby.name}")
            result = self.run_factor(class_name, baby, time_chunk)
            result.rename_axis("Ticker").reset_index()
            # result.rename({"index":"Ticker"})
            c = c.append(result)
            # beta = self.run_factor("Beta",chunk,self.call.market)
            # Pooling function for multiple chunks
        return c

    def stat(self):
        dic = {"Factors": {}}
        counter = 0
        for i in self.factors:
            dic["Factors"]["Factor "+str(counter)]: i.config
            counter += 1
        return dic


"""
data = pd.DataFrame()

#Pooling function for multiple dates
logger.info("Processing Opened")
pool = Pool()
import itertools
args = zip(itertools.repeat(baby,len(time_chunk)), time_chunk)
results = pool.map(self.fetch_class(class_name="Beta"), args)

print(results)

"""

# def import_plugins(self,plugins_package_directory_path, base_class=None, create_instance=True, filter_abstract=True):

#     plugins_package_name = os.path.basename(plugins_package_directory_path)

#     # -----------------------------
#     # Iterate all python files within that directory
#     plugin_file_paths = glob.glob(os.path.join(plugins_package_directory_path, "*.py"))

#     for plugin_file_path in plugin_file_paths:
#         plugin_file_name = os.path.basename(plugin_file_path)

#         module_name = os.path.splitext(plugin_file_name)[0]

#         if module_name.startswith("__"):
#             continue

#         # -----------------------------
#         # Import python file
#         try:
#             logger.info(plugin_file_path)
#             module = importlib.import_module("."+module_name,package="src.hedging.factors")
#         except ModuleNotFoundError as e:
#             st.error(e)

#         # -----------------------------
#         # Iterate items inside imported python file

#         for item in dir(module):
#             value = getattr(module, item)
#             if not value:
#                 continue

#             if not inspect.isclass(value):
#                 continue

#             if filter_abstract and inspect.isabstract(value):
#                 continue

#             if base_class is not None:
#                 if type(value) != type(base_class):
#                     continue

#             # -----------------------------
#             # Instantiate / return type (depends on create_instance)

#             yield value() if create_instance else value

# def fetch_class(self,class_name):
#     factor = None
#     for fac in self.find_all_factor():
#         if fac.config["name"]==class_name:
#             factor = fac
#     if not factor:
#         logger.warning(f"No Class Found with name: {class_name}")
#         return None
#     else:
#         return factor
