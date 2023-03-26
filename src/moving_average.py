import pandas as pd
import numpy as np

def moving_average_crossover(data, fast_period=10, slow_period=50):
    # Calculate the fast (short-term) moving average
    data['Fast_MA'] = data['Close'].rolling(window=fast_period).mean()
    
    # Calculate the slow (long-term) moving average
    data['Slow_MA'] = data['Close'].rolling(window=slow_period).mean()
    
    # Initialize the 'Signal' column with zeros
    data['Signal'] = 0
    
    # Generate buy signals (1) when the fast moving average is greater than the slow moving average
    data.loc[data['Fast_MA'] > data['Slow_MA'], 'Signal'] = 1
    
    # Generate sell signals (-1) when the fast moving average is less than the slow moving average
    data.loc[data['Fast_MA'] < data['Slow_MA'], 'Signal'] = -1
    
    # Shift the signal column by 1 to prevent look-ahead bias
    data['Signal'] = data['Signal'].shift(1)
    
    return data

# Assuming 'historical_data' is a pandas DataFrame with 'Date' and 'Close' columns
# Replace this with your own data obtained from an API or CSV file
historical_data = pd.DataFrame({
    'Date': pd.date_range(start='2020-01-01', end='2022-12-31', freq='D'),
    'Close': np.random.rand(731)
})

# Apply the Moving Average Crossover strategy to the historical data
# Modify the 'fast_period' and 'slow_period' parameters as needed
signals = moving_average_crossover(historical_data)
print(signals.tail())
