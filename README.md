# Algorithmic Trading Bots

Simple equity trading strategies that utilize rule based algorithms to engage in live stock market trades.

## Description

Algorithmic trading bots operate utilizing Quant Connect (QC) API or the QC website's interface. There are currently 2 functioning strategies and 1 in development.

The Breakout Strategy works by identifying a "breakout," or period of rapid growth and opening positions (buying shares) at these distinguished times. It then creates a market stop (sell order) for when the stock price exceeds a certain value. This closing price is dynamically updated to account for market volatility and ensures that positions are not closed prematurely, at the cost of minor losses when positions do start to fall. The model was backtested through the QC API and measured a 34.68% return on investment.
<p align="center">
        <img width = "531" height="561" src = "https://raw.githubusercontent.com/Rravishankar1/Algorithmic-Trading/main/Breakout.png">
</p>

The 200-50 Exponential Moving Average (ema) uses a simple momentum strategy to purchase when the previous 50 day ema is larger than the previous 200 day ema, indicating a momentum increase in position values. Positions are closed when the 50 day average falls short of the 200 day average. The model was backtested through the QC API and measured a 39.98% return on investment.
<p align="center">
        <img width = "531" height="561" src = "https://raw.githubusercontent.com/Rravishankar1/Algorithmic-Trading/main/200-50ema.png">
</p>

The Low Exposure, currently being developed, makes far fewer purchases but identifies periods of near guaranteed growth. Positions are opened when the closing price of a stock is below the previous 7 day low and above the 200 day moving average. Positions are then closed when closing price is over the current 7 day high of the equity.


## Getting Started

### Installing

* Run through [Quant Connect website](https://www.quantconnect.com/terminal/)
* Can also be downlaoded locally and run through [LEAN](https://www.lean.io/#topic100.html) 

### Executing program

* Can be backtested within range of available data (see Quant Connect API docs)
* Market strategy can also be run through live data or paper trading alternative
 
* To change start and end date
```
self.SetStartDate(year, month, day)
self.SetEndDate(year, month, day)
```
* To change initial cash amount
```
self.SetCash('USD Amount')
```
*  To change equity being traded and trade rate
```
self.symbol = self.AddEquity("Equity Name", Resolution.Frequency).Symbol
```


## Version History

* Upload 200-50 EMA and Breakout
* Low Exposure model in progress

