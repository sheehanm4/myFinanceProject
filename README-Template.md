# My Python-Finance Project

During Covid and WFM life style, I wanted to learn more about a programming language. I Invested time into learning Python. I enjoyed learning and wanted to apply the basics to a project. Like many 20 something I've been spending free time investing and learning about trading. I've had intereste in Technical Analysis as a visual learning. I wanted to create a project that took these interests and combined them into a functioning class.

## How to Use

Inititate the Object. This will prompt for user inputs. An Example ticker would be SBUX

An Example Period would be '1y'. An Example interval would be '1d'. This would return daily data for the past year.
```
mystock = stock()
```
Generate a set of Relative Strength Index(RSI) data from the input Open,High,Low, Close Data
```
mystock_rsi = ta.get_rsi(mystock.ohlc_data)
```
Create a Plot object with Title
```
myplots = gp.fin_plots(mystock.ohlc_data,'First Plot')
```
Generate the OHLC Plot with a sub plot of the RSI below. Display the Plot.
```
my_first_plot = myplots.get_price_rsi(mystock_rsi)
my_first_plot.show()
```

### Prerequisites

What things you need to install the software and how to install them

```
pandas 
numpy 
plotly.graph_objects
plotly.subplots 
```



