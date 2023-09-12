import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import date, timedelta

# Load stocks symbols
stocks_data = pd.read_csv("stocks_data.csv")
stocks_symbols = stocks_data.symbol

# Set date range for stock data
years = 10
end_date = pd.to_datetime(date.today())
start_date = end_date - timedelta(days=years*365)

# Fetch stock price data for each symbol and store in a DataFrame
stocks_price = pd.DataFrame()
for symbol in stocks_symbols:
  stock_data = yf.download(symbol, start=start_date, end=end_date)
  close_price = stock_data.Close
  stocks_price[symbol] = close_price

# Calculate average daily return for each stock
daily_returns = stocks_price.pct_change()
avg_daily_return = daily_returns.mean()

# Create correlation matrix to measure relationships between stock returns
correlation_matrix = daily_returns.corr()

# Find optimal portfolios varying weights using randomization
portfolios = []
for i in range(10000): 
  weights = np.random.random(len(stocks_symbols))
  weights /= np.sum(weights)  
  portfolio_return = np.sum(weights * avg_daily_return)
  # Calculate portfolio risk using correlation matrix and weights
  portfolio_risk = np.dot(weights.T, np.dot(correlation_matrix, weights))
  portfolios.append([portfolio_return, portfolio_risk])

# Create a DataFrame of the calculated portfolios
portfolios = pd.DataFrame(portfolios, columns=["Return", "Risk"])

# Plot efficient frontier by visualizing the portfolios' risk and return
plt.figure(figsize=(10, 6))
plt.scatter(portfolios["Risk"], portfolios["Return"], marker="o", s=10, alpha=0.3, color="#088274")
plt.xlabel("Risk")
plt.ylabel("Daily Return")
plt.title('Efficient Frontier')
plt.show()
