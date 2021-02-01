
import pandas as pd 
import numpy as np

def get_ema(ohlc_df,ema_val):
    '''
    Return Data Frame with an "EMA_{ema_val}" Column

    input dataframe must contain a 'Close' column

    Parameters:

    ohlc_df - a standard Open,High,Low,Close data frame with any
    index.
    
    ema_val - An integer value for the desire EMA Calculation

    '''
    ema = ohlc_df['Close'].ewm(span = ema_val, adjust = False).mean()
    ema_df = pd.DataFrame(ema)
    col_dict = {'Close': 'EMA_{}'.format(ema_val)}
    ema_df.rename( columns = col_dict, errors='raise', inplace = True )
    return ema_df


def get_macd(ohlc_df):
    '''
    Return Data Frame with an Calculated Moving Average Convergence Divergence
    Data Columns. 

    input dataframe must contain a 'Close' column to obtain the 12 and 26 ema

    Parameters:

    ohlc_df - a standard Open,High,Low,Close data frame with any
    index.
    
    '''
    ema_12 = get_ema(ohlc_df,12)
    ema_26 = get_ema(ohlc_df,26)

    macd_df = ema_12.join(ema_26)

    macd_df['diff_12_26'] = macd_df.iloc[:,0] - macd_df.iloc[:,1]
    macd_df['MACD EMA'] = macd_df.iloc[:,2].ewm(span = 9,adjust = False).mean()

    return macd_df



def get_rsi(ohlc_df): 
    '''
    The Following code for RSI was taken, and repurposed, from a 
    stackoverflow comment that addressed the smoothing in calculating RSI 
    compared to the more commonly known calculation.

    https://stackoverflow.com/a/24103477
    '''
    
    prices = ohlc_df['Close']
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
        'Date' : ohlc_df.index,
        'Prices' : prices,
        'RSI' : rsi_series
    }
    
    wilder_rsi_df = pd.DataFrame(wilder_rsi_dict, columns = [
    'Prices',
    "RSI"])

    return wilder_rsi_df