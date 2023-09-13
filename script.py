import pandas as pd
import numpy as np
import yfinance as yf
from matplotlib import pyplot as plt, ticker as mtick
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

# Annualize returns
annualized_returns = (1 + avg_daily_return) ** 252 - 1

# Create correlation matrix to measure relationships between stock returns
correlation_matrix = daily_returns.corr()

# Find optimal portfolios varying weights using randomization
num_portfolios = 10000
results = np.zeros((4, num_portfolios))
for i in range(num_portfolios): 
  weights = np.random.random(len(stocks_symbols))
  weights /= np.sum(weights)  
  portfolio_return = np.sum(weights * annualized_returns)
  # Calculate portfolio risk using correlation matrix and weights
  portfolio_risk = np.dot(weights.T, np.dot(correlation_matrix, weights))
  portfolio_risk = np.sqrt(portfolio_risk)
  
  results[0, i] = portfolio_return
  results[1, i] = portfolio_risk
  results[2, i] = portfolio_return / portfolio_risk
  results[3, i] = weights.mean()

# Create a DataFrame of the calculated portfolios
portfolios = pd.DataFrame(
    results.T,
    columns=["Return", "Risk", "Sharpe Ratio", "Weighted Mean"]
)

# Fin the portfolio with the highest Sharpe ratio
max_sharpe_portfolio =  portfolios.iloc[portfolios["Sharpe Ratio"].idxmax()]

# Plot efficient frontier by visualizing the portfolios' risk and return
plt.figure(figsize=(10, 6))
plt.scatter(portfolios["Risk"], portfolios["Return"], c=portfolios["Sharpe Ratio"], cmap="viridis", marker="o", s=10, alpha=0.3)
plt.scatter(max_sharpe_portfolio["Risk"], max_sharpe_portfolio["Return"], color="red", marker="*", s=100, label="Max Sharpe Ratio Portfolio")
plt.xlabel("Risk")
plt.ylabel("Annualized Return")
plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter(1.0))  
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
plt.title("Efficient Frontier with Sharpe Ratios")
plt.colorbar(label="Sharpe Ratio")
plt.legend()
plt.show()