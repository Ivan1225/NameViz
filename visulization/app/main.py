# json library
import json

# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

# Each tab is drawn by one script
from graphs.sample import sample_tab
from graphs.network import network_tab
from graphs.barChart import barChart_tab

# load data and preprocess data
data_source = join(dirname(__file__), 'data', 'sample.json')
with open(data_source, "r") as read_file:
    data = json.load(read_file)

# Create each of the tabs: network, table
tab0 = sample_tab(data)
tab1 = network_tab(data)
tab2 = barChart_tab(data)

# Put all the tabs into one application
tabs = Tabs(tabs=[tab0, tab1, tab2])

# Put the tabs in the current document for display
curdoc().add_root(tabs)