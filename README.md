# Portfolio Optimization Using Python

## Project Description:

This project aims to perform a comprehensive analysis of a selection of 40 stocks that represent the weight distribution by sector of the S&P 500 index. We evaluate various portfolios to understand the impact of different asset weights on the expected return, risk, and Sharpe ratio. The main objective is to compare the optimized portfolios (Max Sharpe Ratio, Max Return, and Min Risk) against the original distribution and derive insights on sector weighting's influence on portfolio performance.

## Key Features:

- **Data Analysis**: Utilizes historical stock price data to calculate returns, risk, and correlations.
- **Portfolio Optimization**: Employs randomization to generate thousands of portfolio combinations and identifies optimal portfolios based on the Sharpe ratio, maximum return, and minimum risk criteria.
- **Visualization**: Provides intuitive visualizations, including an efficient frontier plot and pie/bar charts to illustrate portfolio compositions.

Tools and Libraries Used:
- Python
- Pandas
- NumPy
- Matplotlib
- yfinance

## How to Run the Project:
1. Clone the repository:
``` 
git clone <repository-url>
``` 

2. Navigate to the project directory and install the required libraries:
``` 
cd <project-directory>
pip install -r requirements.txt
```

3. Run the Jupyter Notebook:
``` 
jupyter notebook
``` 

4. Open the portfolio-optimization.ipynb notebook and run all cells.

## Project Structure:
- **data/**: Contains the dataset with information about the selected stocks including symbols and sectors.
- **colors.py**: A Python script to manage the colors associated with different sectors in visualizations.
- **portfolio_plotter.py**: A Python module containing functions for creating portfolio visualizations.
- **portfolio-optimization.ipynb**: The main Jupyter Notebook containing the analysis, visualizations, and insights.

## Results:
The project provides insights into the trade-offs between risk and return and the role of sector allocation in shaping a portfolio's performance. The Max Sharpe Ratio and Max Return portfolios are inclined towards the technology sector, indicating its significance in enhancing returns, while the Min Risk Portfolio is characterized by a more balanced sector distribution to mitigate risk.