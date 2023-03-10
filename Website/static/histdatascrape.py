# -*- coding: utf-8 -*-
"""HistDataScrape.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NsbHaf1ATBwpC2aEgnNKbO50deeJjvQm

Collecting data: I intend to capture the investment and loan data from Yahoo Finance websites as a data source, basically every dimension and every format of data is available to facilitate the later operation. Yahoo has gone to a Reactjs front end which means if you analyze the request headers from the client to the backend you can get the actual JSON they use to populate the client side stores.

Formatting data: Here I will divide the acquired data into xls, csv, sql, and pandas DataFrame format data, and operate them separately to cope with various data source formats

Cleaning and organizing data: excel, sql, python, javascript will be used

Statistical Analysing data: mainly using pandas and sql in python.

Visualize data: I will use django web development for visualisation (html, css, javascript)

As I am responsible for the Collection Part.
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install yfinance
# Import packages
import re
import json
import csv
from io import StringIO
from bs4 import BeautifulSoup
import requests
import yfinance as yf
import pandas as pd

# url templates
url_stats = 'https://finance.yahoo.com/quote/{}/key-statistics?p={}'
url_profile = 'https://finance.yahoo.com/quote/{}/profile?p={}'
url_financials = 'https://finance.yahoo.com/quote/{}/financials?p={}'

# the stock I want to scrape
stock = 'F'

response = requests.get(url_financials.format(stock, stock))
soup = BeautifulSoup(response.text, 'html.parser')
pattern = re.compile(r'\s--\sData\s--\s')
script_data = soup.find('script', text=pattern)

#print(soup)
#print(script_data)

dfFin=yf.download("^SP500-40",period = "1d", interval="5m", rounding = True)
dfTech = yf.download("^SP500-45", period = "1d", interval="5m", rounding = True)
#Data Frame with open, close, lowest and highest price
dfFin = dfFin.loc[:,['Open','Close','Low','High']]
dfTech = dfTech.loc[:,['Open','Close','Low','High']]

Techlist = dfTech.values.tolist()
Finlist = dfFin.values.tolist()