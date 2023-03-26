import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from arch import arch_model
from datetime import datetime

# Assuming 'historical_data' is a pandas DataFrame with 'Date' and 'Close' columns
# You can replace this with your own data obtained from an API or CSV file
historical_data = pd.DataFrame({
    'Date': pd.date_range(start='2010-01-01', end='2022-12-31', freq='D'),
    'Close': np.random.rand(4749)
})

# Calculate daily log returns
historical_data['Log_Returns'] = np.log(historical_data['Close'] / historical_data['Close'].shift(1))

# Fit GARCH model on the log returns
model = arch_model(historical_data['Log_Returns'].dropna(), vol='Garch', p=1, q=1)
garch_fit = model.fit()

# Forecast the volatility
forecast = garch_fit.forecast(horizon=5)  # Forecast 5 days ahead
volatility_forecast = np.sqrt(forecast.variance.dropna())

# Plot the volatility forecast
plt.figure(figsize=(10, 5))
plt.plot(historical_data['Date'][1:], historical_data['Log_Returns'][1:], label='Log Returns')
plt.plot(volatility_forecast.index, volatility_forecast.values, label='Volatility Forecast', color='red')
plt.legend(loc='upper left')
plt.xlabel('Date')
plt.ylabel('Volatility')
plt.title('GARCH Model Volatility Forecast')
plt.show()
