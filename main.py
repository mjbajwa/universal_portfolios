import pandas as pd

from optimal_rebalanced_hindsight import hindsight_constantly_rebalanced_portfolio, \
    plot_optimal_hindsight_rebalanced_portfolio
from two_stock_causal_portfolio import optimal_rebalancing_strategy, postprocess_output_for_two_stocks, \
    plot_wealth_multiplier, plot_portfolio_allocation
from util import plot_stock_performance, compute_price_relatives


def universal_simulation(stock_1, stock_2):

    stocks = [stock_1, stock_2]

    # Load Stock Data

    df_stocks = pd.read_csv("./data/stock_prices_8.csv")
    df_stocks["Cash"] = 1
    df_stocks_relatives = compute_price_relatives(df_stocks)

    prelim_stock = plot_stock_performance(df_stocks, stocks,
                                          title_text="Stock Price",
                                          yaxis_text="Stock Price ($)")

    prelim_multiplier = plot_stock_performance(df_stocks_relatives, stocks,
                                               title_text="Wealth Multiplier",
                                               yaxis_text="Daily Wealth Multiple")

    # Optimal Constantly Rebalanced

    df_hindsight, optimal_alloc, best_multiplier = hindsight_constantly_rebalanced_portfolio(
        df_stocks_relatives,
        stocks)

    hindsight_optimal = plot_optimal_hindsight_rebalanced_portfolio(df_hindsight, stocks)

    # Universal Portfolios

    universal_wealth_multiple, all_b = optimal_rebalancing_strategy(df_stocks_relatives, stocks)

    df_wealth_multiplier, df_portfolio_weight = postprocess_output_for_two_stocks(
        df_stocks_relatives, stocks, df_stocks, universal_wealth_multiple, all_b)

    universal_multiplier = plot_wealth_multiplier(df_wealth_multiplier, stocks)
    universal_allocation = plot_portfolio_allocation(df_portfolio_weight, stocks)

    # prelim_stock, prelim_multiplier, hindsight_optimal, universal_multiplier, universal_allocation

    return universal_multiplier


if __name__ == "__main__":
    universal_simulation("AMZN", "AAPL")
    print("Successfully completed")
