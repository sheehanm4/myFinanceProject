
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Row import Row
from requests.api import options
import stocks_2 as stk
import get_plots as gp
import pandas as pd


summary = ['Symbol','shortName','sector','industry','marketCap','ask','bid','open','regularMarketOpen','previousClose','dayLow', 'dayHigh','fiftyTwoWeekLow', 'fiftyTwoWeekHigh','pegRatio']
header1 = summary[0]
stock_data = ['MSFT','Microsoft Corporation', 'Technology','Software—Infrastructure',2426328055808,323.78,323.75,316,316,310.11,316,326.0973,199.62,326.1,2.27]
header2 = stock_data[0]
data = {header1:summary[1:],header2:stock_data[1:]}
summary_df = pd.DataFrame.from_dict(data)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

#Layout
#---------------------------------------------------



app.layout = dbc.Container([

    dbc.Row([
        dbc.Col(html.H1('My Stock Marker Dashboard', className= 'text-center mb-4'),
                width= 12)
    ]),

    dbc.Row([
        dbc.Col([
            dbc.InputGroup([dbc.InputGroupText("Search", class_name='btn btn-primary'),dbc.Input(placeholder="VOO...")],class_name = 'mb-2 border border-white'),
            dcc.Graph(id='line-fig', figure={}),

            dbc.Label('Time Frame'),
                dbc.RadioItems(id = 'timeframe', options=[
                {"label": "Day ", "value": 1},
                {"label": "Week", "value": 2},
                {"label": "Month", "value": 3},
                {"label": "6 Month", "value": 4},
                {"label": "Year", "value": 5},
                {"label": "5 Year", "value": 6},
                ],
                value=5,
                inline=True),

            dbc.Label('Indicators'),
                dbc.Checklist(id="indicators", options=[
                {"label": "EMA", "value": 1},
                {"label": "RSI", "value": 2},
                {"label": "MACD", "value": 3},
                {"label": "TBD", "value": 4}
                ],
                inline=True,
                value=[],
                switch=True),

        ],width = {'size':8}),

        dbc.Col([
            dbc.Table(id = 'stock_table',bordered=True,dark=True,hover=True,responsive=True,striped=True).from_dataframe(df = summary_df)
        ], width=4)

    ]),

    dbc.Row([

    ])
])


'''
bordered=True,
dark=True,
hover=True,
responsive=True,
striped=True,
'''

'''
app.layout = html.Div( children=[
    html.H1(children='Hello Dash', style = heading_style),
    html.Div(children = [
        html.Div(children='STONKS'),
        html.Div(children='A Web Application that helps look at Technical Charts for Stonks.')
    ],
    style = heading_style
    ),

    html.Div(children = [
        html.Label('Search Stonks',style={'color': colors['text']}),
        html.Div(dcc.Input(id='ticker_input',value= 'Search', type='text',style={'color': colors['text']})),
        html.Button('Submit', id='submit-val', n_clicks=0,style={'color': colors['text'],'backgroundColor': colors['background']})
        ],
       style={'padding': 10, 'flex': 1} 
    ),
            
    
    html.Div(
        children=[
        html.Label('Period',style={'color': colors['text']}),
        dcc.Dropdown(id = 'period-dropdown',options=[
            {'label': '1 Year', 'value': '1y'},
            {'label': '1 Day', 'value': '1d'},],
            value='Select',
            style={'padding': 10, 'flex': 1}
        ),
        html.Label('Interval',style={'color': colors['text']}),
        dcc.Dropdown(id = 'interval-dropdown',options=[
            {'label': '1 Day', 'value': '1d'},
            {'label': '1 Minute', 'value': '1m'}],
            value='Select',
            style={'padding': 10, 'flex': 1}
        ),
        ],
        style={'display': 'flex', 'flex-direction': 'row'}
    ),  

    dcc.Graph(
        id='stock-graph',
        figure = {},
        style={'color': colors['text'],'backgroundColor': colors['background']}
    )
        ]
)


@app.callback(
    Output(component_id ='stock-graph',component_property = 'figure'),
    Input(component_id ='submit-val', component_property = 'n_clicks'),
    State('period-dropdown','value'),
    State('interval-dropdown','value'),
    State(component_id = 'ticker_input', component_property = 'value')
    )
def query_ticker(n_clicks,period_val,interval_val, ticker):

    if ticker == 'Search':
        raise PreventUpdate
    mystock = stk.stock(ticker)
    mystock.ohlc_data_reset(interval_val,period_val)
    mystock.set_ohlc_data()
    
    #Generate the Plot
    myplot = gp.fin_plots(mystock.ohlc_data,'My plot')

    #Get the plot type I want
    myfig = myplot.get_plot_volume()
    return myfig
'''

if __name__ == '__main__':
    app.run_server(debug=True, port= 3000)
    #app.run_server(dev_tools_hot_reload=False)