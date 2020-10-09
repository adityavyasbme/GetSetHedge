import streamlit as st
import datetime
import pandas as pd
import statsmodels.api as sm
import yfinance as yf
from src.helper import load_file


class Beta():

    def __init__(self, baby, market_name="^GSPC"):
        self.baby = baby
        self.market_name = "^GSPC"
        self.config = {
            "name": "Beta",
            "required_days": 30,
            "extra_requirements": []
        }

    def calculate(self, date):
        stat = False

        DD = datetime.timedelta(days=self.config["required_days"])
        last_date = date-DD

        market, _ = load_file("data/index_csv/market.pkl")
        mask = (market.index >= last_date) & (market.index < date)
        market = market.loc[mask]
        market = market["Adj Close"].reset_index(name=self.market_name)

        # try:
        #     market = self.func(market_name,start_date=last_date, end_date = date)
        #     market = market["Adj Close"].reset_index(name=market_name)
        # except:
        #     print("Error in Market")

        if last_date not in self.baby.data.index:
            data = yf.download(self.baby.name, start=last_date, end=date)
        else:
            mask = (self.baby.data.index > last_date) & (
                self.baby.data.index < date)
            data = self.baby.data.loc[mask]

        if len(data) == 0 or len(market) == 0:
            return {"Date": date, self.baby.name: None}

        data = data["Adj Close"].reset_index(name=self.baby.name)
        data = pd.merge(left=data, right=market, how='inner')
        data = data.set_index("Date")
        # calculate monthly returns
        monthly_returns = data.pct_change(1)
        clean_monthly_returns = monthly_returns.dropna(axis=0)

        # split dependent and independent variable
        X = clean_monthly_returns[self.market_name]
        y = clean_monthly_returns[self.baby.name]

        # Add a constant to the independent value
        X1 = sm.add_constant(X)

        # make regression model
        model = sm.OLS(y, X1)

        # fit model and print results
        results = model.fit()
        # print(results.summary())
        if stat:
            st.write(
                f"Start: {last_date} End: {date}"
            )
        return {"Date": date, self.baby.name: results.params[self.market_name]}
