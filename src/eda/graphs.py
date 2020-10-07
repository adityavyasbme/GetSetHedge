#Has a class to plot a graph 
import altair as alt
import streamlit as st
import os
import pandas as pd

class Graph():

	def plot_multiple_tickers(self,parent):
		a = st.multiselect("Plot Multiple Tickers",parent.everyone_names())
		target = st.selectbox("Target Variable",parent.get_feature_list())
		g_cb1 =  st.button('Plot')
		if g_cb1:
			return self.plot_multi(a,parent,target)
		else:
			st.stop()

	def plot_multi(self,names,parent,target):
		childs = []
		source = pd.DataFrame()
		for name in names:
			temp = parent.fetch_child_by_name(name)[0]
			child = parent.children[temp]
			data = child.data[target]
			name = pd.Series([child.name]*len(child.data))
			name.index = data.index

			dic = {"symbol":name,target:data}
			temp = pd.concat(dic,axis=1)
			source = source.append(temp)

		source.reset_index(level=0,inplace=True)
		st.write(source)
		c = alt.Chart(source).mark_line().encode(
											    x='Date',
											    y=target,
											    color='symbol',
											    strokeDash='symbol',
											)
		st.altair_chart(c, use_container_width=True)

		





#Vs a target variable

#Histogram Plotter