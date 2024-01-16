from matplotlib import pyplot as plt
from colors import sector_colors

# Function to create the figure for a given portfolio
def create_portfolio_figure(portfolio_weights, portfolio_stats, title, stocks_symbols, symbol_to_sector):
    # Sort the sectors and stocks by weights in descending order for the pie and bar charts
    sorted_sector_indexes = portfolio_weights['sector_weights'].argsort()[::-1]
    sorted_stock_indexes = portfolio_weights['stock_weights'].argsort()[::-1]
    
    sorted_sectors = portfolio_weights['sector_weights'].index[sorted_sector_indexes]
    sorted_stocks = stocks_symbols[sorted_stock_indexes]
    
    sorted_sector_weights = portfolio_weights['sector_weights'][sorted_sector_indexes]
    sorted_stock_weights = portfolio_weights['stock_weights'][sorted_stock_indexes]

    # Extract the colors in the order of the sectors for the pie chart
    pie_colors = [sector_colors[sector] for sector in sorted_sectors]

    # Create figure for the portfolio
    fig, axs = plt.subplots(1, 2, figsize=(18, 6))

    # Plot the pie chart for sector weights with specific colors
    wedges, texts = axs[0].pie(sorted_sector_weights, startangle=140, colors=pie_colors)
    axs[0].set_title(f"Sector Weights - {title}")

    # Improve pie chart labels using a legend with percentage
    labels = [f'{label}: {value*100:.1f}%' for label, value in zip(sorted_sectors, sorted_sector_weights / sorted_sector_weights.sum())]
    axs[0].legend(wedges, labels, title="Sectors", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    # Get colors for each bar based on its sector for the bar chart
    bar_colors = [sector_colors[symbol_to_sector[symbol]] for symbol in sorted_stocks]

    # Plot the bar chart for stock weights with specific colors for each sector
    bars = axs[1].bar(sorted_stocks, sorted_stock_weights, color=bar_colors)
    axs[1].set_xlabel("Stocks")
    axs[1].set_ylabel("Weights (%)")
    axs[1].set_title(f"Stock Weights - {title}")
    axs[1].tick_params(axis='x', rotation=90)

    # Add portfolio statistics as text
    portfolio_info = (f"{title}\n"
                      f"Return: {portfolio_stats['Return']*100:.2f}%\n"
                      f"Risk: {portfolio_stats['Risk']*100:.2f}%\n"
                      f"Sharpe Ratio: {portfolio_stats['Sharpe Ratio']*100:.2f}%")

    fig.text(0.8, 0.8, portfolio_info, fontsize=12, verticalalignment='top', horizontalalignment='left')

    # Adjust subplots layout
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.7)

    # Print figure
    plt.show()


