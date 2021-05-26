# My Python-Finance Project

During Covid and WFM life style, I wanted to learn more about a programming language. I Invested time into learning Python. I enjoyed learning and wanted to apply the basics to a project. Like many 20 something I've been spending free time investing and learning about trading. I've had intereste in Technical Analysis as a visual learning. I wanted to create a project that took these interests and combined them into a functioning class.

## How to Use
```
mystock = stock()
```
```
myplots = gp.fin_plots(mystock.ohlc_data,'First Plot')
```
```
mystock_macd = ta.get_macd(mystock.ohlc_data)
```
```
mystock_rsi = ta.get_rsi(mystock.ohlc_data)
```
```
my_first_plot = myplots.get_price_rsi(mystock_rsi)
```
```
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



