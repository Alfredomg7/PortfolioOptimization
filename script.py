import pandas as pd
import numpy as np
import yfinance as yf
from matplotlib import pyplot as plt, ticker as mtick
from datetime import date, timedelta
from colors import sector_colors
from portfolio_plotter import create_portfolio_figure

# Load stocks symbols and sectors
stocks_data = pd.read_csv("data/stocks_data.csv")
stocks_symbols = stocks_data.symbol
stocks_sectors = stocks_data.sector

# Create a dictionary to map symbols to sectors
symbol_to_sector = dict(zip(stocks_symbols, stocks_sectors))

# Count the number of stocks in each sector
sector_counts = stocks_data.sector.value_counts()

# Create a pie chart of the stocks distribution by sector
plt.figure(figsize=(8,8))
plt.pie(sector_counts, labels=sector_counts.index, autopct="%1.1f%%", startangle=140, colors=[sector_colors[sector] for sector in sector_counts.index])
plt.title("Stock Distribution by Sector", y=1.08) # Adjusted the y parameter to move title up
plt.axis("equal")
plt.show()

# Set date range for stock data
years = 10
end_date = pd.to_datetime(date.today())
start_date = end_date - timedelta(days=years*365)

# Fetch stock price data for each symbol and store in a DataFrame
stocks_price = pd.DataFrame()
for symbol in stocks_symbols:
  stock_data = yf.download(symbol, start=start_date, end=end_date)
  close_price = stock_data["Close"]  # Use square brackets for indexing
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
results = np.zeros((3, num_portfolios))
portfolio_weights = []
portfolio_sector_weights = {}

for i in range(num_portfolios): 
  weights = np.random.random(len(stocks_symbols))
  weights /= np.sum(weights)  

  # Calculate portfolio annualized return
  portfolio_return = np.sum(weights * annualized_returns)

  # Calculate portfolio risk using correlation matrix and weights
  portfolio_risk = np.dot(weights.T, np.dot(correlation_matrix, weights))
  portfolio_risk = np.sqrt(portfolio_risk)

  # Calculate sector weights for the portfolio
  sector_weights = {sector: 0 for sector in stocks_sectors.unique()}
  for symbol, weight in zip(stocks_symbols, weights):
    sector = symbol_to_sector[symbol]
    sector_weights[sector] += weight

  # Store the portfolio's sector weights in the dictionary
  portfolio_sector_weights[i] = sector_weights
  
  results[0, i] = portfolio_return
  results[1, i] = portfolio_risk
  results[2, i] = portfolio_return / portfolio_risk
  portfolio_weights.append(weights)
  
# Create a DataFrame of the calculated portfolios
columns = ["Return", "Risk", "Sharpe Ratio"]
portfolios = pd.DataFrame(results.T, columns=columns)
stocks_weights = pd.DataFrame(portfolio_weights, columns=stocks_symbols)
sector_weights = pd.DataFrame(portfolio_sector_weights).T  # Transpose the DataFrame

# Find the portfolio with the highest Sharpe ratio
max_sharpe_portfolio = portfolios.iloc[portfolios["Sharpe Ratio"].idxmax()]
max_sharpe_stock_weights = stocks_weights.iloc[portfolios["Sharpe Ratio"].idxmax()]
max_sharpe_sector_weights = sector_weights.iloc[portfolios["Sharpe Ratio"].idxmax()]

# Find the portfolio with the highest return
max_return_portfolio = portfolios.iloc[portfolios["Return"].idxmax()]
max_return_stock_weights = stocks_weights.iloc[portfolios["Return"].idxmax()]
max_return_sector_weights = sector_weights.iloc[portfolios["Return"].idxmax()]

# Find the portfolio with the lowest risk
min_risk_portfolio = portfolios.iloc[portfolios["Risk"].idxmin()]
min_risk_stock_weights = stocks_weights.iloc[portfolios["Risk"].idxmin()]
min_risk_sector_weights = sector_weights.iloc[portfolios["Risk"].idxmin()]

# Plot efficient frontier by visualizing the portfolios' risk and return
plt.figure(figsize=(10, 6))
plt.scatter(portfolios["Risk"], portfolios["Return"], c=portfolios["Sharpe Ratio"], cmap="viridis", marker="o", s=10, alpha=0.3)
plt.scatter(max_sharpe_portfolio["Risk"], max_sharpe_portfolio["Return"], color="red", marker="*", s=100, label="Max Sharpe Ratio Portfolio")
plt.scatter(max_return_portfolio["Risk"], max_return_portfolio["Return"], color="green", marker="^", s=100, label="Max Return Portfolio")
plt.scatter(min_risk_portfolio["Risk"], min_risk_portfolio["Return"], color="blue", marker="s", s=100, label="Min Risk Portfolio")
plt.xlabel("Risk")
plt.ylabel("Annualized Return")
plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter(1.0))  
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
plt.title("Efficient Frontier with Sharpe Ratios")
plt.colorbar(label="Sharpe Ratio")
plt.legend(loc="lower right")
plt.show()

# Prepare data for Max Sharpe Ratio Portfolio
max_sharpe_data = {
    'sector_weights': max_sharpe_sector_weights,
    'stock_weights': max_sharpe_stock_weights,
}

# Plot weight distribution by sector, by stock and stats for the Max Sharpe Ratio Portfolio
create_portfolio_figure(max_sharpe_data, max_sharpe_portfolio, "Max Sharpe Ratio Portfolio", stocks_symbols, symbol_to_sector)

# Prepare data for Max Return Portfolio
max_return_data = {
    'sector_weights': max_return_sector_weights,
    'stock_weights': max_return_stock_weights,
}

# Plot weight distribution by sector, by stock and stats for the Max Return Portfolio
create_portfolio_figure(max_return_data, max_return_portfolio, "Max Return Portfolio", stocks_symbols, symbol_to_sector)

# Prepare data for Min Risk Portfolio
min_risk_data = {
    'sector_weights': min_risk_sector_weights,
    'stock_weights': min_risk_stock_weights,
}

# Plot weight distribution by sector, by stock and stats for the Min Risk Portfolio
create_portfolio_figure(min_risk_data, min_risk_portfolio, "Min Risk Portfolio", stocks_symbols, symbol_to_sector)

