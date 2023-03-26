import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from arch import arch_model
import alpaca_trade_api as tradeapi
from datetime import datetime

# Replace with your own API key and secret
with open('secrets/secrets.json') as f:
    secrets = json.load(f)
API_KEY = secrets['KEY']
API_SECRET = secrets['SECRET']
BASE_URL = 'https://paper-api.alpaca.markets'  # For paper trading, use the paper trading URL

# Set up the Alpaca API client
api = tradeapi.REST(API_KEY, API_SECRET, base_url=BASE_URL, api_version='v2')
if __name__ == '__main__':
    # Get historical data for the S&P 500 index (using the ETF 'SPY' as a proxy)
    symbol = 'SPY'
    start_date = '2010-01-01'
    end_date = '2022-12-31'
    timeframe = '1D'

    historical_data = api.get_bars(symbol, tradeapi.rest.TimeFrame.Day, start=start_date, end=end_date).df

    # Calculate daily log returns
    historical_data['Log_Returns'] = np.log(historical_data['close'] / historical_data['close'].shift(1))

    # Fit GARCH model on the log returns
    model = arch_model(historical_data['Log_Returns'].dropna(), vol='Garch', p=1, q=1)
    garch_fit = model.fit()

    # Forecast the volatility
    forecast = garch_fit.forecast(horizon=5)  # Forecast 5 days ahead
    volatility_forecast = np.sqrt(forecast.variance.dropna())

    # Plot the volatility forecast
    plt.figure(figsize=(10, 5))
    plt.plot(historical_data.index[1:], historical_data['Log_Returns'][1:], label='Log Returns')
    plt.plot(volatility_forecast.index, volatility_forecast.values, label='Volatility Forecast', color='red')
    plt.legend(loc='upper left')
    plt.xlabel('Date')
    plt.ylabel('Volatility')
    plt.title('GARCH Model Volatility Forecast')
    plt.show()
