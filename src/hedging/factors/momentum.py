import pandas as pd


class Momentum():

    def __init__(self, baby):
        """
        Args:
            baby (obj): Child Object
        """

        self.baby = baby

        # Config parameter
        self.config = {
            "name": "Momentum",
            "required_days": 80,
            "extra_requirements": []
        }

    def calculate(self, date):
        """
        Args:
            date (datetime): Date in focus

        Returns:
            Momentum (pd.DataFrame)
        """
        data = self.baby.data

        if len(data) == 0:
            return pd.DataFrame()

        data = data["Adj Close"]
        data = data.rename(self.baby.name)
        # calculate monthly returns
        monthly_returns = data.pct_change(self.config["required_days"])

        try:
            mask = (self.baby.data.index.date > date)
        except:
            mask = (self.baby.data.index > date)

        monthly_returns = monthly_returns.loc[mask]

        return monthly_returns.T
