import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from main import universal_simulation

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')
available_indicators = df['Indicator Name'].unique()

# Updates for Cover Code

df_stocks = pd.read_csv("./data/stock_prices_8.csv")
df_stocks["Cash"] = 1
available_stocks = [col for col in df_stocks.columns if col != "Date"]

app.layout = html.Div([

    html.Div([
        dcc.Dropdown(
            id='stock_1',
            options=[{'label': i, 'value': i} for i in available_stocks],
            value='AMZN'
        ),
        dcc.Dropdown(
            id='stock_2',
            options=[{'label': i, 'value': i} for i in available_stocks],
            value='Cash'
        )
    ],
        style={'width': '48%', 'display': 'inline-block'}),

    dcc.Graph(id='wealth-multiplier-graphic'),

])


@app.callback(
    Output('wealth-multiplier-graphic', 'figure'),
    [Input('stock_1', 'value'),
     Input('stock_2', 'value')])
def update_graph(stock_1, stock_2):
    fig = universal_simulation(stock_1=stock_1, stock_2=stock_2)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
