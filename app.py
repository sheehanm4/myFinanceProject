
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import stocks_2 as stk
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

    html.Div(dcc.Input(id='ticker_input',value= None, type='text')),
    html.Button('Submit', id='submit-val', n_clicks=0),


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
    Input(component_id ='submit-val', component_property = 'n_clicks'),
    State('period-dropdown','value'),
    State('interval-dropdown','value'),
    State(component_id = 'ticker_input', component_property = 'value')
    )
def query_ticker(n_clicks,period_val,interval_val, ticker):

    if ticker is None:
        raise PreventUpdate
    mystock = stk.stock(ticker)
    mystock.ohlc_data_reset(interval_val,period_val)
    mystock.set_ohlc_data()
    
    #Generate the Plot
    myplot = gp.fin_plots(mystock.ohlc_data,'My plot')

    #Get the plot type I want
    myfig = myplot.get_plot_volume()
    return myfig




if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(dev_tools_hot_reload=False)
