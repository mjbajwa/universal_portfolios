import pandas as pd
import numpy as np
import plotly.graph_objects as go


# Create stock price relatives

def compute_price_relatives(df):
    df = df.copy(deep=True)

    for stock in list(df.columns)[1:]:
        df[stock] = df[stock] / df[stock].shift(+1)

    df = df.iloc[1:, :]

    return df


def plot_stock_performance(df_stocks, stocks, title_text, yaxis_text):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_stocks["Date"],
                             y=df_stocks[stocks[0]],
                             mode='lines',
                             name=stocks[0]))

    fig.add_trace(go.Scatter(x=df_stocks["Date"],
                             y=df_stocks[stocks[1]],
                             mode='lines',
                             name=stocks[1]))

    fig.update_layout(title=title_text, yaxis_title=yaxis_text)

    return fig
