import yfinance as yf
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as  np

#Define any varaibles

ticker_summary = ('symbol','shortName','sector','industry','marketCap','ask',
'bid','open','regularMarketOpen','previousClose','dayLow', 
'dayHigh','fiftyTwoWeekLow', 'fiftyTwoWeekHigh','pegRatio')

global_periods = ('1d','5d','1mo','3mo','6mo','1y','2y','5y','10y', 'ytd','max')
global_intervals = ('1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo')

class stock():


    def __init__(self):
        """
        stock( 'Ticker Symbol String' ). 
        
        This Class is based off of Yfinance and the goal is to pull specific data from
        the Ticker Objects, and re-organize that data into it's own object.
        """
        ticker_symbol = self.get_ticker()
        
        time_inputs = self.get_time()

        #estblish self._this_stock as equivelent to the ticker object
        self._this_stock = yf.Ticker(ticker_symbol)
        #the self._this_stock_info
        self._this_stock_info = self._this_stock.info
        
        self._date_flag = time_inputs['date_flag']
        if time_inputs['date_flag'] == False:
            self.period = time_inputs['period']
        elif time_inputs[0] == True:
            self.start_date = time_inputs['start']
            self.end_date = time_inputs['end']
        else:
            raise AttributeError('Invalid Time Flag! \n')

        self.interval = time_inputs['interval']
    

    def get_bid_ask(self):
        '''
        get_bid_ask ()
        Returns the bid, ask and spread of a stock object in list form
        Returns [bid,ask,spread]
        '''
        ask = self._this_stock_info['ask']
        bid = self._this_stock_info['bid']
        spread = round(abs(ask - bid),3)

        return [bid,ask,spread]

    def summary(self):
        '''
        summary(
        Returns a list of summary data from stock
        '''
        print('Printing Summary of the Ticker...')
        for k in ticker_summary:
            print('{} | {} '.format(k,self._this_stock_info[k]))

    def get_history(self):
        '''
        return a dataframe of historical data based on the acceptable arguments
        of yf.history()

        Parameters: period : 
        str Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y, ytd,max 

        interval : 
        str Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo 
        Intraday data cannot extend last 60 days start: str Download start date 
        string (YYYY-MM-DD) or _datetime. Default is 1900-01-01 end: str 
        Download end date string (YYYY-MM-DD) or _datetime
        '''
        print('Retrieving Data for {} ...'.format(self._this_stock_info[
            'shortName']))

        if self._date_flag == False:
            hist = self._this_stock.history(period = self.period, interval = self.interval)
        else:
            hist = self._this_stock.history(start = self.start_date, end = self.end_date, interval = self.interval)

        return hist

    def get_EMA(self,ema_val = 200):
    
        ohlc_df = self.get_history()

        ema = ohlc_df['Close'].ewm(span = ema_val, adjust = False).mean()
        ema_df = pd.DataFrame(ema)
        col_dict = {'Close': 'EMA_{}'.format(ema_val)}
        ema_df.rename( columns = col_dict, errors='raise', inplace = True )
        return ema_df

    def get_MACD(self):

        ema_12 = self.get_EMA(12)
        ema_26 = self.get_EMA(26)

        macd_df = ema_12.join(ema_26)

        macd_df['diff_12_26'] = macd_df.iloc[:,0] - macd_df.iloc[:,1]
        macd_df['MACD EMA'] = macd_df.iloc[:,2].ewm(span = 9,adjust = False).mean()

        return macd_df

    def get_RSI(self):
        '''
        The Following code for RSI was taken, and repurposed, from a 
        stackoverflow comment that addressed the smoothing in calculating RSI 
        compared to the more commonly known calculation.

        https://stackoverflow.com/a/24103477
        '''

        data = self.get_history()
        print(data.head())
        prices = data['Close']
        print(prices)
        n = 14
        # RSI = 100 - (100 / (1 + RS))
        # where RS = (Wilder-smoothed n-period average of gains / Wilder-smoothed n-period average of -losses)
        # Note that losses above should be positive values
        # Wilder-smoothing = ((previous smoothed avg * (n-1)) + current value to average) / n
        # For the very first "previous smoothed avg" (aka the seed value), we start with a straight average.
        # Therefore, our first RSI value will be for the n+2nd period:
        #     0: first delta is nan
        #     1:
        #     ...
        #     n: lookback period for first Wilder smoothing seed value
        #     n+1: first RSI

        # First, calculate the gain or loss from one price to the next. The first value is nan so replace with 0.
        deltas = (prices-prices.shift(1)).fillna(0)

        # Calculate the straight average seed values.
        # The first delta is always zero, so we will use a slice of the first n deltas starting at 1,
        # and filter only deltas > 0 to get gains and deltas < 0 to get losses
        print(deltas)
        avg_of_gains = deltas[1:n+1][deltas > 0].sum() / n
        avg_of_losses = -deltas[1:n+1][deltas < 0].sum() / n

        # Set up pd.Series container for RSI values
        rsi_series = pd.Series(0.0, deltas.index)

        # Now calculate RSI using the Wilder smoothing method, starting with n+1 delta.
        up = lambda x: x if x > 0 else 0
        down = lambda x: -x if x < 0 else 0
        i = n+1
        for d in deltas[n+1:]:
            avg_of_gains = ((avg_of_gains * (n-1)) + up(d)) / n
            avg_of_losses = ((avg_of_losses * (n-1)) + down(d)) / n
            if avg_of_losses != 0:
                rs = avg_of_gains / avg_of_losses
                rsi_series[i] = 100 - (100 / (1 + rs))
            else:
                rsi_series[i] = 100
            i += 1

        #Conver 0s to NaNs
        rsi_series = np.where(rsi_series == 0, np.nan,rsi_series)

        wilder_rsi_dict = {
            'Date' : data.index,
            'Prices' : prices,
            'RSI' : rsi_series
        }
        
        wilder_rsi_df = pd.DataFrame(wilder_rsi_dict, columns = [
        'Prices',
        "RSI"])
        return wilder_rsi_df

    def get_ticker(self):
        while True:
            ticker = input('What Symbol Are you Interested in? \n' )  
            #Check to make sure ticker Sumbol is valid
            #Check that a string was entered

            #Check that a valid symbol was entered
            try:
                print('...Processing...')
                symbolData = yf.Ticker(ticker)
                name = symbolData.info['shortName']
                type(name) == str 
                #Print the Symbol is valid
                print('The stock Ticker, {}, entered is valid....\n'.format(ticker))
                break

            except:
                print('The Entered Value is not valid, Try Again. \n')
                continue
        return ticker

    def get_time(self):
        format = "%Y-%m-%d"
        response = dict(date_flag = False)
        while True:

            choice = input('Do you want to input a generic time period or a start and end date?'
            ' Enter in "generic" or "dates" to select? \n')

            if choice == 'generic':

                while True:
                    time_period = input('What is the desired Time period? The Possible options are:'
                    ' 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max. \n')
                    if time_period in global_periods:
                        print('The Time Period is Valid \n')
                        response['period'] = time_period
                        break
                    else:
                        print('The Time Period Entered is Not valid \n')
                        continue

            elif choice == 'dates':
                
                response['date_flag'] = True
                while True:
                    start_date = input(' What is the desired Start Date? Desired format is (YYYY-MM-DD) \n')
                    try:
                        datetime.datetime.strptime(start_date, format)
                        print("This is the correct date string format. \n")
                        response['start'] = start_date
                        break
                    except ValueError:
                        print("This is the incorrect date string format. It should be YYYY-MM-DD \n")
                        continue
                
                while True:

                    end_date = input(' What is the desired End Date? Desired format is (YYYY-MM-DD) \n')
                    try:
                        datetime.datetime.strptime(end_date, format)
                        print("This is the correct date string format. \n")
                        response['end'] = end_date
                        break
                    except ValueError:
                        print("This is the incorrect date string format. It should be YYYY-MM-DD \n")
                break
            else:
                print('Argument is not valid, Enter in a value again.')
                continue

            while True:
                time_interval = input('What is the desired Time Interval? The Possible options are:'
                ' 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo. Intraday data cannot extend last 60 days \n')
                if time_interval in global_intervals:
                    print('The Time Interval is Valid \n')
                    response['interval'] = time_interval
                    break
                else:
                    print('The Time Interval is Not Valid')
                    continue
            break

        return response





def main():

    mystock = stock()



if __name__ == '__main__': main()