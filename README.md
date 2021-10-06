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

1. Run the Stock.py Script

' ' '
/.stock.py
' ' ' 

2. Enter in a valid Stock Symbol

3. Type a Period from the choices

4. Type a Interval from the choices

```ruby
require 'redcarpet'
markdown = Redcarpet.new("Hello World!")
puts markdown.to_html
``` 

## Sample Run

'''

python .\stocks.py
What Symbol Are you Interested in? 
> MSFT
...Processing...
The stock Ticker, MSFT, entered is valid....

Do you want to input a generic time period or a start and end date? Enter in "generic" or "dates" to select?
> generic
What is the desired Time period? The Possible options are: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max. 
> 1y
The Time Period is Valid 

What is the desired Time Interval? The Possible options are: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo. Intraday data cannot extend last 60 days
> 1d
The Time Interval is Valid 

Retrieving Data for Microsoft Corporation ...
'''

## Acknowledgments

* yfinace Maintainer Ran Aroussi
* stackoverflow contributor 

