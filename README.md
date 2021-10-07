# My Python-Finance Project

During Covid and WFM life style, I wanted to learn more about a programming language. I invested time into learning Python. I enjoyed learning and wanted to apply the basics to a project. Like many 20 something I've been spending free time investing and learning about trading. I took interest in Technical Analysis, also known as TA. I wanted to create a project that took my interests and combined them into a functioning class.

I view this project as something of a precursor to what could be a better script for automatically generating analysis for a symbol based on simple inputs. I work on it to that end. 


### Prerequisites

# Libraries that will be needed

- pandas 
- numpy
- plotly
- yfinance


### Using the Scripts

1. Initiate the Stock object that is based on yfiance ticker

```
import stocks
import ta_analysis as ta
import get_plots as gp

mystock = stocks.stock()
```

2. Enter in a valid Stock Symbol

3. Type a Period from the choices

4. Type a Interval from the choices

5. Use the Attribute Open, High, Low, Close data to create a Plot Object
```
myplots = gp.fin_plots(mystock.ohlc_data,'First Plot')
```
6. Use the Technical Analsis Script to get relevant Data for your plot
```
mystock_macd = ta.get_macd(mystock.ohlc_data)
mystock_rsi = ta.get_rsi(mystock.ohlc_data)
```
7. Make your plot and show it.
```
my_first_plot = myplots.get_price_rsi(mystock_rsi)
my_first_plot.show()
```

# Sample Plot

![This is an image](https://github.com/sheehanm4/myFinanceProject/blob/dc9da5c0817f1ffc4a2f7529063af541ff7b6a95/sample.png)


### Acknowledgments

* yfinace Maintainer Ran Aroussi
* stackoverflow contributor 

