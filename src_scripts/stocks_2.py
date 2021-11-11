'''
This stock class is creating a ticker object with out inheriting all the methods and properties
Testing using inheritance resulted in errors due to the Ticker CLass alone does not
have all the attributes neccessary to perform a couple key methods. For the sake of building out
the rest of the application and features, it is easier to instantiate the class this way.
'''

import yfinance as yf
from yfinance.utils import empty_df
import ta_analysis as ta


#Define varaibles
ticker_summary = ('symbol','shortName','sector','industry','marketCap','ask',
'bid','open','regularMarketOpen','previousClose','dayLow', 
'dayHigh','fiftyTwoWeekLow', 'fiftyTwoWeekHigh','pegRatio')
global_periods = ('1d','5d','1mo','3mo','6mo','1y','2y','5y','10y', 'ytd','max')
global_intervals = ('1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo')

class stock():


    def __init__(self,ticker_symbol):
        """
        stock(). 
        
        """
        #Create the This Stock attribute from yf
        self._this_stock = yf.Ticker(ticker_symbol)
        #get some basic information
        self.info = self._this_stock.info
        #set a period  and interval from which to pull and graph data
        self.period = '1y'
        self.interval = '1d'
        #retrieve the Open,High,Low,Close Data for the given interval
        self.set_ohlc_data()

    def get_bid_ask(self):
        '''
        get_bid_ask ()
        Returns the bid, ask and spread of a stock object in list form
        Returns [bid,ask,spread]
        '''
        ask = self.info['ask']
        bid = self.info['bid']
        spread = round(abs(ask - bid),3)
        return [bid,ask,spread]

    def summary(self):
        '''
        summary(
        Returns a list of summary data from stock
        '''
        my_summary = {}
        for k in range(len(ticker_summary)):
            my_summary[ticker_summary[k]] = self._this_stock.info[ticker_summary[k]]
        return my_summary

    #Set a new period
    def __set_period__(self,new_period):
        self.period = new_period

    #set a new interval
    def __set_interval__(self,new_interval):
        self.interval = new_interval

    #Query for the OHLC Data
    def set_ohlc_data(self):
        self.ohlc_data = self._this_stock.history(period = self.period,interval = self.interval)

    #Get the current OHLC Data
    def get_ohlc(self):
        return self.ohlc_data

    #Query OHLC Data with new period and interval
    def ohlc_data_reset(self,new_interval,new_period):
        self.__set_interval__(new_interval)
        self.__set_period__(new_period)

    def get_macd(self):
        return ta.get_macd(self.ohlc_data)

    def get_rsi(self):
        return ta.get_rsi(self.ohlc_data)

    def get_ema(self,ema_val = 200):
        return ta.get_ema(self.ohlc_data,ema_val)

    def get_divi(self):
        if self._this_stock.dividends.empty:
            return None
        else:
            divi_df = self._this_stock.dividends[-4:]
            return divi_df

    def get_ebit(self):
        fin_df = self._this_stock.financials
        return fin_df.loc['Ebit':'Ebit',:]
        
        
        


if __name__ == '__main__':
    my_stock = stock('JNJ')
    my_stock.get_bid_ask()
    my_stock.set_ohlc_data()
    

    

