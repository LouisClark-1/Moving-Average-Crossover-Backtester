# Mean Reversion Strategy Backtester
#### Video demo can be found [here](www.youtube.com)
### Description:
This program backtests two strategies on the chosen stock and compares them to the strategy of simply buying and holding the stock for the full duration. It tests over the past year at daily intervals, buying at the close price and holding for the next day before reconsidering. It starts with 1000 of the local curency.
#### Usage:
Use command line arguments to enter your stock ticker. Use the "-t" or "--ticker" flags to pick your chosen stock. If none is entered, the program will exit. If the chosen stock has fewer than 20 days of history the program will exit. If the ticker does not exist, there will be an HTTP 404 error. Make sure to include the exchange suffix on any non-USA stock. For example, RR.L to specify Rolls Royce from the London Stock Exchange. Here's an example usage:
```
python project.py -t MSFT
```
#### Buy and Hold strategy:
Represented by the blue line on the graph, this strategy buys 1000 of the local currency, and holds for the duration of the backtest (1 year).
#### Binary strategy:
Represented by the red line, this strategy calculates the 20 day and 5 day moving averages. If on a particular day, the 5 day average is above the 20 day average, the stock will be bought at the close price and held for the next day. If the 5 day average is below the 20 day average, the stock is sold / kept as cash and there will be no gain or loss on the next day.
#### Variable strategy:
Represented by the green line, this strategy changes what proportion of the investment is held in the stock or as cash on the next day. This decision is bsed on percentage difference of the 5 day moving average relative to the 20 day moving average (referred to as x). The higher this number, the more confidently we can say theres an uptrend so the more money we are willing to commit to the stock.
|   x%           | % invested |
| :------------: | :--------: |
| x < -0.5       | 0          |
| -0.5 ≤ x < 0.5 | 25         |
| 0.5 ≤ x < 1.5  | 50         |
| 1.5 ≤ x < 2.5  | 75         |
| 2.5 ≤ x        | 100        |
#### Text output:
The program also outputs the total return for the 3 strategies over the year. For example:
> Holding saw 6.3% change, the binary strategy saw a 30.9% change, and the variable strategy saw a 54.1% change. (IONQ)