
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
#flex Styles
heading_style={
        'textAlign': 'center',
        'color': colors['text'],
        'backgroundColor': colors['background']
        }


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

if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(dev_tools_hot_reload=False)