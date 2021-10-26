
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import stocks_2 as stk
import ta_analysis as ta
import get_plots as gp

app = dash.Dash(__name__)

colors = {
    'background': '#504A4B',
    'text': '#7FDBFF'
}


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for your data.', style={
        'textAlign': 'center',
        'color': colors['text']}),

    html.Br(),
    html.Label('My Stock'),
    dcc.Input(id = 'ticker_input',value='Ticker', type='text'),
    
    html.Div(children=[
    html.Label('Stock'),
    dcc.Dropdown(
        id = 'stock-dropdown',
        options=[
            {'label': 'Startbucks', 'value': 'sbux'},
            {'label': 'Microsoft', 'value': 'msft'},
            ],value='Select')]),   

    html.Div(children=[
        html.Label('Period'),
        dcc.Dropdown(
            id = 'period-dropdown',
            options=[
                {'label': '1 Year', 'value': '1y'},
                {'label': '1 Day', 'value': '1d'},
                ],value='Select')]),

    html.Div(children=[
        html.Label('Interval'),
        dcc.Dropdown(
            id = 'interval-dropdown',
            options=[
                {'label': '1 Day', 'value': '1d'},
                {'label': '1 Minute', 'value': '1m'}],
            value='Select')]),
       
    dcc.Graph(
        id='stock-graph',
        figure = {})
])

@app.callback(
    Output(component_id ='stock-graph',component_property = 'figure'),
    [Input(component_id = 'stock-dropdown',component_property = 'value')],
    prevent_initial_call = True
)
def get_my_fig(input_val):
    print('callback')
    mystock = stk.stock(input_val)
    
    #Generate the Plot
    myplot = gp.fin_plots(mystock.ohlc_data,'My plot')

    #Get the plot type I want

    myfig = myplot.get_price_vol_prof()
    return myfig

if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(dev_tools_hot_reload=False)
