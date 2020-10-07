"""Home page shown when the user enters the application"""
import streamlit as st

import awesome_streamlit as ast


# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading About ..."):
        st.write(
        f"# Get Set Hedge")
        st.write(
        "** Synthetic Hedging of Security via Corresponding Factor ETFs **")
        st.write(
        "Given the rise of assets under passive management and particularly because of rise of ETFs, stock prices might be driven based on the ETF performance of ETF’s that the stock is part of, in addition to the underlying business fundamentals. Get Set Hedge is a framework which a discretionary investor might want to use in case he likes a certain stock but does not like certain factors it is exposed to. The way we do this is by pre-creating multiple academic factors and allowing the investor to request for building a custom factor (at some price of course). Get Sed Hedge perform historical factor validation analysis and produce robust hedges the investor needs to do. In order to execute those hedges in market an investor can use relevant ETFs. We also provide hedge execution services to our premium clients at subscription basis."
        )
        st.markdown(
            """**Home Page**
""",
            unsafe_allow_html=True,
        )
