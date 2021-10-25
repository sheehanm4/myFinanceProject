
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import stocks
import ta_analysis as ta
import get_plots as gp

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

#bring in data
mystock = stocks.stock()

#Generate the Plot
myplot = gp.fin_plots(mystock.ohlc_data,'My plot')

#Get the plot type I want
myfig = myplot.get_plot_base()

app = dash.Dash(__name__)

colors = {
    'background': '#504A4B',
    'text': '#7FDBFF'
}


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for your data.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Br(),
    html.Label('My Stock'),
    dcc.Input(value='Ticker', type='text'),

    html.Div(children=[
        html.Label('Period'),
        dcc.Dropdown(
            options=[
                {'label': '1 Year', 'value': '1y'},
                {'label': '1 Day', 'value': '1d'},
            ],
            value='Select'
        ),

    html.Div(children=[
        html.Label('Interval'),
        dcc.Dropdown(
            options=[
                {'label': '1 Day', 'value': '1d'},
                {'label': '1 Minute', 'value': '1m'}],
            value='Select'
        ),
        
    dcc.Graph(
        id='My Stock Sample',
        figure=myfig)
    ])
])
])

if __name__ == '__main__':
    app.run_server(dev_tools_hot_reload=False)