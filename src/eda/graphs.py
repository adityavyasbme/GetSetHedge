# Has a class to plot a graph
import altair as alt
import streamlit as st
import pandas as pd


class Graph():
    """Class to plot graphs
    """

    def plot_multiple_tickers(self, parent):
        """Function to plot multiple columns into single graph using altair lib
        Args:
            parent (object): Parent class's object
        """
        a = st.multiselect("Plot Multiple Tickers", parent.everyone_names())
        target = st.selectbox("Target Variable", parent.get_feature_list())
        g_cb1 = st.button('Plot')
        if g_cb1:
            return self.plot_multi(a, parent, target)
        else:
            st.stop()

    def plot_multi(self, names, parent, target):
        """sub function of plot_multiple_tickers function;
        It Fetches  the data from the parent and plot it.

        Args:
            names (list): List of names of ticker
            parent (obj): Parent Class object
            target (str): target variable
        """
        source = pd.DataFrame()
        for name in names:
            temp = parent.fetch_child_by_name(name)[0]
            child = parent.children[temp]
            data = child.data[target]
            name = pd.Series([child.name]*len(child.data))
            name.index = data.index

            dic = {"symbol": name, target: data}
            temp = pd.concat(dic, axis=1)
            source = source.append(temp)

        source.reset_index(level=0, inplace=True)
        st.write(source)
        c = alt.Chart(source).mark_line().encode(
            x='Date',
            y=target,
            color='symbol',
            strokeDash='symbol',
        )
        st.altair_chart(c, use_container_width=True)
# TODO: Vs a target variable

# TODO: Histogram Plotter
