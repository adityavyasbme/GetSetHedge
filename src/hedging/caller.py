import logging
import yfinance as yf
from src.helper import create_logger, dump_file
from src.hedging.division import Division

import datetime

logger = create_logger('Caller', 'logs/Hedging.log',
                       logging.DEBUG, logging.WARNING)


class Caller(Division):
    """Caller class that inherits the property of divison class to divide data
    Args:
        Division (class): Inheritance
    """

    def __init__(self, govt, location):
        """
        Args:
            govt (obj): Government Object
            location (list/dic): location of tracked population of parent
        """
        self.gov = govt
        self.loc = location
        self.parent = self.gov.population[self.loc[0]]
        self.market_pulled = False

    def call_parent(self):
        """
        Returns:
            Parent (object)
        """
        return self.parent

    def pull_childs_in_range(self, start=datetime.datetime(2019, 1, 1), end=datetime.datetime(2019, 1, 31)):
        """Wrapper function that pulls all the child in a Range

        Args:
            start (date, optional): [description]. Defaults to datetime.datetime(2019, 1, 1).
            end (date, optional): [description]. Defaults to datetime.datetime(2019, 1, 31).

        Returns:
            List of childs or None, if not found.
        """
        logger.info("Pulling All childrens")
        try:
            return self.parent.fetch_all_child_in_range(start, end)
        except:
            return None

    def pull_market(self):
        """
        Pull the index's data

        Returns:
            returns Market data and also saves it into a pickle file for caching.
        """
        new = self.parent.start_date-datetime.timedelta(days=100)
        self.market = yf.download('^GSPC', start=new, end=self.parent.end_date)
        self.market_pulled = True
        dump_file("data/index_csv/market.pkl", self.market)
        return self.market

    def stat(self):
        """Statistics function for monitoring.
        """
        dic = {"Market Pulled": self.market_pulled}
        return dic
