import streamlit as st
import datetime
import pandas as pd


class Momentum():

    config = {
    "name" : "Momentum",
    "required_days" : 30,
    "extra_requirements":[]
    }

    def __init__(self,baby,market_name="^GSPC"):
        self.baby = baby
        self.market_name="^GSPC"

    def calculate(self,date):
        stat= False

        DD = datetime.timedelta(days=config["required_days"])
        last_date = date-DD

        if last_date not in self.baby.data.index:
            data = pd.DataFrame()
        else:
            mask = (self.baby.data.index > last_date) & (self.baby.data.index < date)
            data= self.baby.data.loc[mask]

        if len(data)==0 or len(market)==0:
            return {"Date":date,self.baby.name:None}

        data = data["Adj Close"].reset_index(name=self.baby.name)
        data = data.set_index("Date")

        # calculate monthly returns
        monthly_returns = data.pct_change(30)
        return monthly_returns.T

