"""
This script Runs the front-end of the Streamlit application.
"""
import src.pages.about
import src.pages.gallery.index
import src.pages.home
import src.pages.data
import src.pages.hedging
import streamlit as st
import awesome_streamlit as ast

PAGES = {
    "Home": src.pages.home,
    "Input": src.pages.gallery.index,
    "Viz": src.pages.data,
    "Hedging": src.pages.hedging,
    "Documentation": src.pages.about,
}


def main():
    '''
    Frontend of Streamlit App.
    '''
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]
    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)
    st.sidebar.title("Contribute")
    st.sidebar.info(
        "This an open source project and you are very welcome to **contribute** your awesome "
        "comments, questions, resources and apps as "
        "[issues](https://github.com/adityavyasbme/GetSetHedge/issues) of or "
        "[pull requests](https://github.com/adityavyasbme/GetSetHedge/pulls) "
        "to the [source code](https://github.com/adityavyasbme/GetSetHedge). "
    )
    st.sidebar.title("About")
    st.sidebar.info(
        """
        This app is maintained by Aditya Vyas. You can learn more about Adi at
        [linkedin.com](https://linkedin.com/in/adityavyasbme)."""
    )
