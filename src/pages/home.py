"""Home page shown when the user enters the application"""
import streamlit as st

from PIL import Image

try:
    virginia = Image.open('data/images/virginia.jpg')
except:
    st.error("Error in Reading Images. Please check data/images Folder.")


def write():
    """Front End of the About Page
    """
    with st.spinner("Loading About ..."):
        st.write(
            f"# Get Set Hedge")
        st.write(
            "**Synthetic Hedging of Security via Corresponding Factor ETFs**")
        st.write(
            "Given the rise of assets under passive management and particularly because of rise of ETFs, stock prices might be driven based on the ETF performance of ETF’s that the stock is part of, in addition to the underlying business fundamentals."
        )
        st.image(virginia,
                 use_column_width=True)
        st.markdown("<center><a href='https://www.darden.virginia.edu/sites/default/files/inline-files/Matos%20The%20Growth%20of%20Passive%20Investing%20Worldwide.pdf'>Source: University of Virginia</a></center>", unsafe_allow_html=True)

        st.write(
            "Get Set Hedge is a framework which a discretionary investor might want to use in case he likes a certain stock but does not like certain factors it is exposed to."
        )
        st.write(
            "The way we do this is by pre-creating multiple academic factors and allowing the investor to request for building a custom factor(at some price of course)."
        )
        st.write(
            "Get Set Hedge perform historical factor validation analysis and produce robust hedges the investor needs to do. In order to execute those hedges in market an investor can use relevant ETFs."
        )
        st.write(
            "We also provide hedge execution services to our premium clients at subscription basis."
        )
