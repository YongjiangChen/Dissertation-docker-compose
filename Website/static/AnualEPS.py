import json
import requests

CURR_YEAR = 2022
equityNum = 0
DATA_RANGE = 10
listYearFirmEPS = []

def appendData(dataList, rawData):
    for i in range(DATA_RANGE):
        l1 = []
        l1.append(CURR_YEAR-i)
        l1.append(equityNum)
        l1.append(rawData['annualEarnings'][i]['reportedEPS'])
        dataList.append(l1)

url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=AAPL&apikey=YATGD1ZK2W3CERBT'
r = requests.get(url)
data = r.json()
#appendData(listYearFirmEPS, data)


url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=MSFT&apikey=YATGD1ZK2W3CERBT'
r = requests.get(url)
data = r.json()
equityNum = 1
#appendData(listYearFirmEPS, data)

url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=GOOGL&apikey=YATGD1ZK2W3CERBT'
r = requests.get(url)
data = r.json()
equityNum = 2
#appendData(listYearFirmEPS, data)

url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=AMZN&apikey=YATGD1ZK2W3CERBT'
r = requests.get(url)
data = r.json()
equityNum = 3
#appendData(listYearFirmEPS, data)

url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=META&apikey=YATGD1ZK2W3CERBT'
r = requests.get(url)
data = r.json()
equityNum = 4
#appendData(listYearFirmEPS, data)

listYearFirmEPS.reverse()
#print(listYearFirmEPS)

TOP5_EQUITY_EPS = [[2013, 4, '0.87'], [2014, 4, '1.73'], [2015, 4, '2.28'], [2016, 4, '4.24'], [2017, 4, '5.39'], [2018, 4, '7.57'], 
[2019, 4, '6.44'], [2020, 4, '10.1'], [2021, 4, '13.8'], [2022, 4, '5.18'], [2013, 3, '0.58'], [2014, 3, '-0.54'], [2015, 3, '1.24'],
 [2016, 3, '4.91'], [2017, 3, '4.56'], [2018, 3, '20.13'], [2019, 3, '23.01'], [2020, 3, '6.86'], [2021, 3, '3.25'], [2022, 3, '-0.58'],
  [2013, 2, '1.0975'], [2014, 2, '1.279'], [2015, 2, '1.479'], [2016, 2, '1.717'], [2017, 2, '1.6005'], [2018, 2, '2.185'], [2019, 2, '2.459'],
   [2020, 2, '2.9435'], [2021, 2, '5.62'], [2022, 2, '2.44'], [2013, 1, '2.63'], [2014, 1, '2.46'], [2015, 1, '2.76'], [2016, 1, '3.3'], [2017, 1, '3.88'], 
   [2018, 1, '4.75'], [2019, 1, '5.75'], [2020, 1, '8.05'], [2021, 1, '9.2'], [2022, 1, '0'], [2013, 0, '1.415'], [2014, 0, '1.6075'], [2015, 0, '2.3'], [2016, 0, '2.0675'],
    [2017, 0, '2.3'], [2018, 0, '2.97'], [2019, 0, '2.98'], [2020, 0, '3.27'], [2021, 0, '5.62'], [2022, 0, '4.82']]

##########################################################################################################################################
#import yfinance as yf
#import pandas as pd


#sp500 = yf.Ticker('^SP500-45')
#sp500_hist = sp500.history(period='1d', interval='1d')
#sp500_hist.to_csv('sp500_1y.csv')
#result = sp500_hist.to_json(orient="records")
#print(result)