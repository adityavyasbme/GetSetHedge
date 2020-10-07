import streamlit as st

import awesome_streamlit as ast


# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading About ..."):
        st.write(
        f"# Application Basket for ML in Finance")
        st.markdown(
            """**About Page**
""",
            unsafe_allow_html=True,
        )
