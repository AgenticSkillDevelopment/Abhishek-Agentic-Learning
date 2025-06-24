# stock_analysis.py

import yfinance as yf
import matplotlib.pyplot as plt

# Define stock and period
ticker = "TSLA"
period = "ytd"

# Download data
data = yf.download(ticker, period=period)

# Calculate percentage change
data['YTD Gain %'] = (data['Close'] - data['Close'].iloc[0]) / data['Close'].iloc[0] * 100

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(data.index, data['YTD Gain %'], label=f'{ticker} YTD Gain %')
plt.title(f'{ticker} YTD Stock Gain')
plt.xlabel("Date")
plt.ylabel("YTD Gain (%)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
