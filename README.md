# Algorithmic Trading Bots

Simple trading bots that utilize rule based algorithms to engage in live stock market trades.

## Description

Algorithmic trading bots operate utilizing Quant Connect (QC) API or the QC website's LEAN interface. There are currently 2 functioning bots and 1 in development.

The Breakout Strategy bot works by identifying a "breakout," or period of rapid growth and opening positions (buying shares) at these distinguished times. It then creates a market stop (sell order) for when the stock price exceeds a certain value. This closing price is dynamically updated to account for market volatility and ensures that positions are not closed prematurely, at the cost of minor losses when positions do start to fall. The model was backtested through the QC API and measured a 34.68% return on investment.
<div style="text-align:center"><img src="/Breakout.png" width="750">
![](/Breakout.png)

The 200-50 Exponential Moving Average (ema) bot uses a simple momentum strategy to purchase when the previous 50 day ema is larger than the previous 200 day ema, indicating a momentum increase in position values. Positions are closed when the 50 day average falls short of the 200 day average. The model was backtested through the QC API and measured a 39.98% return on investment.
![](/200-50ema.png)

The Low Exposure bot, currently being developed, makes far fewer purchases but identifies periods of near guaranteed growth. Positions are opened when the closing price of a stock is below the previous 7 day low and above the 200 day moving average. Positions are then closed when closing price is over the current 7 day high of the equity.


## Getting Started

### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* Upload 200-50 EMA and Breakout
* Low Exposure model in progress

