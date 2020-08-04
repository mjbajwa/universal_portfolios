import pandas as pd
import numpy as np
import plotly.graph_objects as go


def cumulative_wealth_multiple(df_stocks_relatives, b_1, stocks):
    # What is the optimal constantly rebalanced portfolio allocation b = [b1, 1-b1],
    # such that the compounded growth is maximized?

    """
    b1: Amount of stock 1 (as ranked in stocks) in the portfolio
    """

    b_2 = 1 - b_1
    b = np.array([b_1, b_2])

    x_1 = np.array(df_stocks_relatives[stocks[0]])
    x_2 = np.array(df_stocks_relatives[stocks[1]])

    x_matrix = np.vstack((x_1, x_2))
    period_returns = np.array(np.matmul(b, x_matrix))

    return np.prod(period_returns)


def hindsight_constantly_rebalanced_portfolio(df_stocks_relatives, stocks):
    frac_stock_1 = np.arange(0, 1.01, 0.01)
    wealth_multiple_hindsight = np.array([cumulative_wealth_multiple(df_stocks_relatives=df_stocks_relatives,
                                                                     b_1=b_stock_1, stocks=stocks) for b_stock_1 in
                                          frac_stock_1])

    df_hindsight = pd.DataFrame(data={"fraction": frac_stock_1,
                                      "wealth_multiple": wealth_multiple_hindsight})

    optimal_alloc_1 = df_hindsight.iloc[df_hindsight['wealth_multiple'].idxmax(), 0]
    best_hindsight_multiplier = df_hindsight['wealth_multiple'].max()

    return df_hindsight, optimal_alloc_1, best_hindsight_multiplier


def plot_optimal_hindsight_rebalanced_portfolio(df_hindsight, stocks):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_hindsight["fraction"],
                             y=df_hindsight["wealth_multiple"],
                             mode='markers+lines',
                             name=stocks[0]))

    fig.update_layout(title="Wealth Multiplier of Constantly Rebalanced Portfolio in Hindsight",
                      yaxis_title="Wealth Multiple at the end of period",
                      xaxis_title="Fraction of Portfolio in " + stocks[0])

    return fig

