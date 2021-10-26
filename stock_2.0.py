import yfinance as yf


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
        self._this_stock = yf.Ticker(ticker_symbol)
        self.period = '1y'
        self.interval = '1d'
        self.ohlc_data = self._this_stock.history(period = self.period,interval = self.interval)
        self.info = self._this_stock.info

    def get_bid_ask(self):
        '''
        get_bid_ask ()
        Returns the bid, ask and spread of a stock object in list form
        Returns [bid,ask,spread]
        '''
        ask = self._this_stock.info['ask']
        bid = self._this_stock.info['bid']
        spread = round(abs(ask - bid),3)
        return [bid,ask,spread]

    def summary(self):
        '''
        summary(
        Returns a list of summary data from stock
        '''
        print('Printing Summary of the Ticker...')
        for k in ticker_summary:
            print('{} | {} '.format(k,self.info[k]))


if __name__ == '__main__':
    my_stock = stock('MSFT')
    my_stock.summary()