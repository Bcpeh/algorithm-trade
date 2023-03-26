import alpaca_trade_api as tradeapi
import json

with open('secrets.json') as f:
    secrets = json.load(f)
API_KEY = secrets['KEY']
API_SECRET = secrets['SECRET']

api = tradeapi.REST(
        API_KEY,
        API_SECRET,
        'https://paper-api.alpaca.markets'
    )

# Get our account information.
account = api.get_account()

# Check if our account is restricted from trading.
if account.trading_blocked:
    print('Account is currently restricted from trading.')

# Check how much money we can use to open new positions.
print('${} is available as buying power.'.format(account.buying_power))

if __name__ == '__main__':
    """
    With the Alpaca API, you can check on your daily profit or loss by
    comparing your current balance to yesterday's balance.
    """

    # First, open the API connection
    
    # Get account info
    account = api.get_account()

    # Check our current balance vs. our balance at the last market close
    balance_change = float(account.equity) - float(account.last_equity)
    print(f'Today\'s portfolio balance change: ${balance_change}')