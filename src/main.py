import requests
import json

# Replace with your own API key and secret
with open('secrets.json') as f:
    secrets = json.load(f)
API_KEY = secrets['KEY']
API_SECRET = secrets['SECRET']
BASE_URL = 'https://paper-api.alpaca.markets'  # For paper trading, use the paper trading URL


# Function to get the account information
def get_account():
    url = f'{BASE_URL}/v2/account'
    headers = {
        'APCA-API-KEY-ID': API_KEY,
        'APCA-API-SECRET-KEY': API_SECRET
    }

    response = requests.get(url, headers=headers, verify=False)
    return json.loads(response.content)


# Function to get the stock's latest trading price
def get_latest_trade(symbol):
    url = f'{BASE_URL}/v2/stocks/{symbol}/trades/latest'
    headers = {
        'APCA-API-KEY-ID': API_KEY,
        'APCA-API-SECRET-KEY': API_SECRET
    }

    response = requests.get(url, headers=headers)
    return json.loads(response.content)


# Function to get the stock's historical trading prices
def get_historical_prices(symbol, timeframe, start_date, end_date):
    url = f'{BASE_URL}/v2/stocks/{symbol}/bars'
    headers = {
        'APCA-API-KEY-ID': API_KEY,
        'APCA-API-SECRET-KEY': API_SECRET
    }

    params = {
        'timeframe': timeframe,
        'start': start_date,
        'end': end_date
    }

    response = requests.get(url, headers=headers, params=params)
    return json.loads(response.content)


if __name__ == '__main__':
    # Replace 'AAPL' with the symbol of the stock you want to target
    symbol = 'AAPL'

    account_info = get_account()
    print('Account Information:', account_info)

    latest_trade = get_latest_trade(symbol)
    print('Latest Trade:', latest_trade)

    # Replace the date range with your desired range
    historical_prices = get_historical_prices(symbol, '1D', '2022-01-01', '2022-12-31')
    print('Historical Prices:', historical_prices)
