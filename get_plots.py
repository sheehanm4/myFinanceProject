import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ta_analysis as ta

colors = {
    'background': '#504A4B',
    'text': '#7FDBFF'
}

class fin_plots():


    def __init__(self,input_data,title):
        '''
        fin_plots().

        This Class creates simple instance of a plot with base data used to create a Technical Chart and a Title. 

        The Methods generate the desired Chart using plotly. 
        
        Example:

        my_plots = fin_plots(ohlc_ddf,' My Chart ')
        plot1 = myplots.get_plot_base()
        plot1.show()

        '''
        self.data = input_data
        self.title = title


        pass

    def get_plot_base(self):
        '''
        Returns a Basic Candle Stick plot with the data that was instantiated with the fin_plot object. 

        No Parameters

        Returns a Plotly Figure
        '''

        input_df = self.data

        fig = go.Figure(data=[go.Candlestick(x=input_df.index,
                                            open=input_df['Open'],
                                            high=input_df['High'],
                                            low=input_df['Low'],
                                            close=input_df['Close'],
                                            name = 'Price')])

        fig.update_xaxes( rangebreaks=[
        dict(bounds=["sat", "mon"]), #hide weekends
        dict(values=["2015-12-25", "2016-01-01"])  # hide Christmas and New Year's
        ])

            
        fig.update_layout( title = self.title,
                            yaxis_title = 'Price',
                            xaxis_title = 'Time',
                            plot_bgcolor = colors['background'])              
        return fig
    
    def get_plot_volume(self):
        '''
        Returns a Basic Candle Stick plot with the data that was instantiated with the fin_plot object. Provides Volume histogram subplot. 

        No Parameters

        Returns a Plotly Figure
        '''
        input_df = self.data
        fig = make_subplots(rows=2, cols=1,row_heights=[1,0.3],shared_xaxes=True)

        fig.append_trace(go.Candlestick(x=input_df.index,
                        open=input_df['Open'],
                        high=input_df['High'],
                        low=input_df['Low'],
                        close=input_df['Close'],name = 'Price'),row=1, col=1)    
        fig.append_trace(go.Bar(x=input_df.index, y = input_df['Volume'],name = 'Volume'),row=2, col=1)
        fig.update_layout(height=800, width=800, title_text=self.title)
        fig.update_yaxes(title_text="Price", showgrid=False, row=1, col=1)
        fig.update_yaxes(title_text="Volume", showgrid=False, row=2, col=1)
        return fig
   
    def get_plot_ema(self,ema1,ema2):
        '''
        get_plot_volume_ema(ema1,ema2)

        Returns a Basic Candle Stick plot with the data that was instantiated with the fin_plot object. Provides plotting for Only 2 EMAs. 

        Parameters
        EMA1/EMA2 - a dataframe of EMAs. Works with ta_analysis.py 

        Returns a Plotly Figure
        '''

        input_df = self.data
        ema1_name = str(ema1.columns[0])
        ema2_name = str(ema2.columns[0])
        fig = go.Figure(data=[go.Candlestick(x=input_df.index,
                                    open=input_df['Open'],
                                    high=input_df['High'],
                                    low=input_df['Low'],
                                    close=input_df['Close'],name = 'Price'),
                go.Scatter(x=ema1.index, y=ema1[ema1_name],name = ema1_name, line=dict(color='orange', width=1)),
                go.Scatter(x=ema2.index, y=ema2[ema2_name],name = ema2_name, line=dict(color='green', width=1))])

        fig.update_layout(height=800, width=800, title_text="Price with {} and {}".format(ema1_name,ema2_name))      
        return fig 

    def get_plot_volume_ema(self,ema1,ema2):
        '''
        get_plot_volume_ema(ema1,ema2)

        Returns a Basic Candle Stick plot with the data that was instantiated with the fin_plot object. Provides plotting for Only 2 EMAs with a Volume Histogram Subplot.

        Parameters
        EMA1/EMA2 - a dataframe of EMAs. Works with ta_analysis.py 

        Returns a Plotly Figure
        '''
        input_df = self.data
        ema1_name = str(ema1.columns[0])
        ema2_name = str(ema2.columns[0])
        fig = make_subplots(rows=2, cols=1,row_heights=[1,0.3],shared_xaxes=True)
        fig.append_trace(go.Candlestick(x=input_df.index,
                        open=input_df['Open'],
                        high=input_df['High'],
                        low=input_df['Low'],
                        close=input_df['Close'],name = 'Price'),row=1, col=1)
        fig.append_trace(go.Scatter(x=ema1.index, y=ema1[ema1_name], line=dict(color='orange', width=1)),row=1, col=1)
        fig.append_trace(go.Scatter(x=ema2.index, y=ema2[ema2_name], line=dict(color='green', width=1)),row=1, col=1)
        fig.append_trace(go.Bar(x=input_df.index, y = input_df['Volume'], name = 'Volume'),row=2, col=1)
        fig.update_layout(height=800, width=800, title_text="Price and Volume")

        return fig
        
    def get_price_vol_prof(self):
        '''
        Returns a Volume Profile using the Volume data provided with a OHLC Data input used to instantiate the fin_plot object. 

        No Parameters

        Returns a Plotly figure
        '''

        input_df = self.data
        resolution = 25.00
        price_max = round(input_df['Close'].max(),2)
        price_min = round(input_df['Close'].min(),2)
        price_diff = round(price_max - price_min,2)
        price_widths = round(price_diff/resolution,2)

        price_list=[]
        for i in range(26):
            price_list.append(price_min + (price_widths*i))
        
        sum_vol = {}
        for j in range(25):
            total_vol = 0
            for i in (input_df.index):
                if (input_df.loc[i,'Close'] > price_list[j]) & (input_df.loc[i,'Close'] < price_list[j+1]):
                    total_vol += input_df.loc[i,'Volume']
                else:
                    continue
            
            sum_vol[j] = (price_list[j] ,price_list[j+1],total_vol)
        
        price_vol_df = pd.DataFrame.from_dict(sum_vol,orient='index',
                       columns=['Price_Min', 'Price_Max', 'Total Volume'])

        fig = go.Figure(data=[go.Bar(x=price_vol_df['Total Volume'],y = price_vol_df['Price_Min'], 
                        orientation='h')])

        
        return fig

    def get_price_macd(self,macd_df):
        '''
        get_plot_price_macd(macd_df)

        Returns a Basic Candle Stick plot with the data with a subplot of the Moving Average Covergence Divergence(MACD) indicator graph. 

        Parameters:
        MACD dataframe idealy created with the get_macd() method of the ta_analysis.py script


        Returns a Plotly Figure
        '''
        input_df = self.data
        macd_df['hist_color'] =  np.where(macd_df['hist']<0, 'red', 'green')
        fig = make_subplots(rows=2, cols=1,row_heights=[1,.5],shared_xaxes=True)

        fig.append_trace(go.Candlestick(x=input_df.index,
                        open=input_df['Open'], high=input_df['High'],
                        low=input_df['Low'], close=input_df['Close']),row=1, col=1)

        fig.append_trace(go.Scatter(x=macd_df.index , y = macd_df['MACD EMA'],name = 'MACD EMA'), row=2, col=1)

        fig.append_trace(go.Scatter(x=macd_df.index , y = macd_df['diff_12_26'],name = 'MACD'), row=2, col=1)

        fig.append_trace(go.Bar(x=macd_df.index , y = macd_df['hist'],name = 'DIFF',marker_color=macd_df['hist_color']), row=2, col=1)

        fig.update_layout(xaxis_rangeslider_visible=False,height=800, width=1000, xaxis={'type': 'category'})

        return fig

    def get_price_rsi(self,rsi_df):
        '''
        get_price_rsi(rsi_df)
        Returns a candlestick plot with a Relative Stregth Index(RSI) subplot.

        Parameters: Dataframe of Relative strength index formatted in the get_rsi method of ta_analysis.py.

        Returns a Plotly Figure

        '''
        input_df = self.data

        fig = make_subplots(rows=2, cols=1,row_heights=[1,.5],shared_xaxes=True)

        fig.append_trace(go.Candlestick(x=input_df.index,
                        open=input_df['Open'], high=input_df['High'],
                        low=input_df['Low'], close=input_df['Close']),row=1, col=1)

        fig.append_trace(go.Scatter(x=rsi_df.index , y = rsi_df['RSI'],name = 'RSI'), row=2, col=1)
        fig.add_hline(y=30,row=2, col=1)
        fig.add_hline(y=70,row=2, col=1)
        fig.add_hrect(y0=30, y1=70, line_width=0, fillcolor="green", opacity=0.2,row=2, col=1)
        fig.update_yaxes(range=[10, 90],row=2, col=1)
        fig.update_layout(xaxis_rangeslider_visible=False,height=800, width=1000, xaxis={'type': 'category'})
        return fig

