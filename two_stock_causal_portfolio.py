import numpy as np
import pandas as pd
import plotly.graph_objects as go


def wealth_k(b_k, x_k):
    """
    b_k = [b_1_k, b_2_k] portfolio allocation at time step k
    x_k = [x_1_k, x_2_k]^k wealth multiplier at time step k
    """

    return np.prod(np.matmul(b_k, x_k))


def wealth_n(b_n, x_n, n):
    """
    Computes the final wealth factor after n steps

    b_n = list containing arrays of b_k
    x_k = observed wealth multiplier of sequences
    """
    product_term = []

    for k in range(1, n + 1):
        b_k = b_n[k - 1]
        x_k = x_n[:, k - 1]
        product_term.append(np.matmul(b_k, x_k))

    result = np.prod(np.array(product_term))

    return result


def b_next(x_n, k, number_of_splits=20):
    """
    Rebalanced portfolio of securities at each time steps (only for m = 2)

    The integral over interval [0,1] is split into "number_of_splits" chunks

    x_n = matrix of relative performance (m x n : m stocks and n days)
    k = index of current timestep
    number_of_splits = controls the resolution of the integration
    """

    # Calculate Numerator and Denominator

    numerator_terms = []
    denominator_terms = []

    for i in range(0, number_of_splits + 1):
        b_i = np.array([i / number_of_splits, 1 - i / number_of_splits])
        x_k = x_n[:, 0:k]  # only up to k is used because we are trying to predict k+1
        numerator_terms.append(i / number_of_splits * wealth_k(b_i, x_k))
        denominator_terms.append(wealth_k(b_i, x_k))

    weighted_num = np.sum(np.array(numerator_terms))
    all_portfolios_denom = np.sum(np.array(denominator_terms))

    return np.array([weighted_num / all_portfolios_denom, 1 - weighted_num / all_portfolios_denom])


def optimal_rebalancing_strategy(df_stocks_relatives,
                                 stocks,
                                 number_of_splits=50,
                                 b_init=np.array([0.50, 0.50])):

    x_1 = np.array(df_stocks_relatives[stocks[0]])
    x_2 = np.array(df_stocks_relatives[stocks[1]])
    x_n = np.vstack((x_1, x_2))

    # Simulate the whole trajectory now.
    # We start with b_0 and obtain consecutive non-anticipating re-balancing portfolios

    all_b = [b_init]

    # Auxillary Variables

    total_runs = x_n.shape[1]
    universal_wealth_multiple = []

    for k in range(1, total_runs + 1):

        if k % 500 == 0:
            print("{} Runs Remaining".format(total_runs - k))

        b_inc = b_next(x_n, k, number_of_splits=number_of_splits)
        all_b.append(b_inc)
        universal_wealth_multiple.append(wealth_n(all_b, x_n, n=k))

    return universal_wealth_multiple, all_b


def postprocess_output_for_two_stocks(df_stocks_relatives, stocks, df_stocks,
                                      universal_wealth_multiple, all_b):
    # Universal Wealth Multiple DataFrame

    x_1 = np.array(df_stocks_relatives[stocks[0]])
    x_2 = np.array(df_stocks_relatives[stocks[1]])
    universal_mult = np.array(universal_wealth_multiple)
    stock_1 = [np.prod(x_1[0:i]) for i in range(1, x_1.shape[0] + 1)]
    stock_2 = [np.prod(x_2[0:i]) for i in range(1, x_2.shape[0] + 1)]

    df_wealth_multiplier = pd.DataFrame(data={"universal_portfolio": universal_mult,
                                              "stock_1_only": stock_1,
                                              "stock_2_only": stock_2
                                              })

    df_wealth_multiplier["Date"] = df_stocks_relatives["Date"]

    # Portfolio Weights

    frac_stock_1 = [b[0] for b in all_b]
    frac_stock_2 = [b[1] for b in all_b]

    df_portfolio_weight = pd.DataFrame(data={stocks[0]: frac_stock_1,
                                             stocks[1]: frac_stock_2})

    df_portfolio_weight["Date"] = df_stocks_relatives["Date"]

    # Minor refurbishing of date column

    df_wealth_multiplier.at[0, "Date"] = df_stocks["Date"][0]
    df_portfolio_weight.at[0, "Date"] = df_stocks["Date"][0]

    return df_wealth_multiplier, df_portfolio_weight


def plot_wealth_multiplier(df_wealth_multiplier, stocks,
                           title_text="Wealth Multiplier", yaxis_text="Multiplier"):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_wealth_multiplier["Date"],
                             y=df_wealth_multiplier["universal_portfolio"],
                             mode='lines',
                             name="Universal Portfolio",
                             marker=dict(color='Black')))

    fig.add_trace(go.Scatter(x=df_wealth_multiplier["Date"],
                             y=df_wealth_multiplier["stock_1_only"],
                             mode='lines',
                             name=stocks[0],
                             marker=dict(color='Red')))

    fig.add_trace(go.Scatter(x=df_wealth_multiplier["Date"],
                             y=df_wealth_multiplier["stock_2_only"],
                             mode='lines',
                             name=stocks[1],
                             marker=dict(color='Blue')))

    fig.update_layout(title=title_text, yaxis_title=yaxis_text)

    return fig


def plot_portfolio_allocation(df_portfolio_weight, stocks,
                              title_text="Portfolio Weight", yaxis_text="Fraction of Portfolio (%) in "):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_portfolio_weight["Date"],
                             y=df_portfolio_weight[stocks[0]],
                             mode='lines',
                             name=stocks[0],
                             marker=dict(color='Red')))

    fig.update_layout(title=title_text, yaxis_title=yaxis_text + stocks[0])

    return fig

