from django.db import models

# Create your models here.
import numpy as np
import pandas as pd
import yfinance as yf
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import matplotlib.pyplot as plt

# download the data
df = yf.download(tickers=['AAPL'], period='10y')
y = df['Close'].fillna(method='ffill')
y = y.values.reshape(-1, 1)

# scale the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaler = scaler.fit(y)
y = scaler.transform(y)

# generate the input and output sequences
n_lookback = 60  # length of input sequences (lookback period)
n_forecast = 30  # length of output sequences (forecast period)

# generate the forecasts
X_ = y[- n_lookback:]  # last available input sequence
X_ = X_.reshape(1, n_lookback, 1)

# load the saved LSTM model
model = load_model('C:/Users/yongj/Desktop/Testing/MiniProject/models/visuallstm_model_nextmonth_apple_100_64.h5')
Y_ = model.predict(X_).reshape(-1, 1)
Y_ = scaler.inverse_transform(Y_)

# organize the results in a data frame
df_past = df[['Close']].reset_index()
df_past.rename(columns={'index': 'Date', 'Close': 'Actual'}, inplace=True)
df_past['Date'] = pd.to_datetime(df_past['Date'])
df_past['Forecast'] = np.nan
df_past['Forecast'].iloc[-1] = df_past['Actual'].iloc[-1]

df_future = pd.DataFrame(columns=['Date', 'Actual', 'Forecast'])
df_future['Date'] = pd.date_range(start=df_past['Date'].iloc[-1] + pd.Timedelta(days=1), periods=n_forecast)
df_future['Forecast'] = Y_.flatten()
df_future['Actual'] = np.nan

plt.figure(figsize=(16,6))
last_90 = pd.concat([df_past, df_future]).iloc[-90:]
last_180 = pd.concat([df_past, df_future]).iloc[-180:]
plt.plot(last_180['Date'], last_180['Actual'], label='Actual')
plt.plot(last_180['Date'], last_180['Forecast'], label='Forecast')

plt.title('Apple Stock Price Prediction')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Apple Stock Price')

# Adjusting the xticks
plt.xticks(rotation=45)
plt.xlim(last_180['Date'].min(), last_180['Date'].max())
xticks = pd.date_range(start=last_180['Date'].min(), end=last_180['Date'].max(), freq='W')
plt.xticks(xticks, xticks.strftime("%b-%d-%Y"))

plt.legend()
plt.show()

# save the plot to an HTML file
filename = 'C:/Users/yongj/Desktop/Testing/MiniProject/templates/stock_price_predictions.html'
plt.savefig(filename)
    
