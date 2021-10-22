import yfinance as yf

#Define varaibles
ticker_summary = ('symbol','shortName','sector','industry','marketCap','ask',
'bid','open','regularMarketOpen','previousClose','dayLow', 
'dayHigh','fiftyTwoWeekLow', 'fiftyTwoWeekHigh','pegRatio')
global_periods = ('1d','5d','1mo','3mo','6mo','1y','2y','5y','10y', 'ytd','max')
global_intervals = ('1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo')

class stock():


    def __init__(self):
        """
        stock(). 
        
        This Class is based off of Yfinance and the goal is to pull specific data from the Ticker Objects, and re-organize that data into it's own object. Then leverage scripts that can perform calculations to help create graphs and display the technical analysis.
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

        self.ohlc_data = self.get_history()
    
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
        str Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max 

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

    def get_ticker(self):
        '''
        Prompts the user to enter a ticker symbol from which to pull data from and 
        check the validity of the input. 

        Example input would be 'SBUX'
        '''
        while True:
            ticker = input('What Symbol Are you Interested in? \n' )  
            
            #Check that a string was entered
            try:
                type(ticker) == str
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
            except:
                print('The Entered Value is not a string, Try Again. \n')
                continue

        return ticker

    def get_time(self):
        ''' Generate a user interface to define the time inputs

            Time inputs can either be previous amount of tiome from present OR a pre-defined
            date period
        '''
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


