import stocks
import ta_analysis as ta
import get_plots as gp




def main():

    mystock = stocks.stock()
    myplots = gp.fin_plots(mystock.ohlc_data,'First Plot')
    mystock_macd = ta.get_macd(mystock.ohlc_data)
    mystock_rsi = ta.get_rsi(mystock.ohlc_data)
    my_first_plot = myplots.get_price_rsi(mystock_rsi)
    my_first_plot.show()



if __name__ == '__main__': main()