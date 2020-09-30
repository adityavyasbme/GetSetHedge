"""Main module for the streamlit app"""
import streamlit as st

import awesome_streamlit as ast
import src.pages.about
import src.pages.gallery.index
import src.pages.home
import src.pages.data
import src.pages.hedging

ast.core.services.other.set_logging_format()

PAGES = {
    "Home": src.pages.home,
    "Data": src.pages.data,
    "AutoML": src.pages.gallery.index,
    "Hedging": src.pages.hedging,
    "About": src.pages.about,
}


def main():
    """Main function of the App"""
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)
    st.sidebar.title("Contribute")
    st.sidebar.info(
        "This an open source project and you are very welcome to **contribute** your awesome "
        "comments, questions, resources and apps as "
        "[issues](https://www.google.com) of or "
        "[pull requests](https://www.google.com) "
        "to the [source code](https://www.google.com). "
    )
    st.sidebar.title("About")
    st.sidebar.info(
        """
        This app is maintained by Aditya Vyas. You can learn more about me at
        [linkedin.com](https://linkedin.com/in/adityavyasbme)."""
    )


if __name__ == "__main__":
    main()