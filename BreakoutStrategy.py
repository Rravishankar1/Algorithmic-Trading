import numpy as np

class BreakoutStrategy(QCAlgorithm):
    """
    Breakout volatility model
    
    Opens positions when crossing previous highs (breakouts).
    Uses volatility factor to determine when significant decreases occur.
    Closes positions during said falls.
    """

    def Initialize(self):
        """
        Initializes base conditions: date for backtesting, purchase frequency, 
        lookback length, and risk factors.
        """
        
        # Data Resolution
        self.SetStartDate(2011,1,7)
        self.SetEndDate(2015,1,7)
        self.SetCash(100000)
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        # Base lookback length, ceiling and floor for adjustability
        self.lookback = 20
        self.ceiling, self.floor = 28, 12
        
        # Distance (as percents) indicative of fall
        self.initialStopRisk = 0.96
        self.trailingStopRisk = 0.92
        
        # Schedule function 20 minutes after every market open
        self.Schedule.On(self.DateRules.EveryDay(self.symbol), \
                        self.TimeRules.AfterMarketOpen(self.symbol, 20), \
                        Action(self.EveryMarketOpen))


    def OnData(self, data):
        """Method to plot closing prices over time."""
        
        # Plot data
        self.Plot("Data Chart", self.symbol, self.Securities[self.symbol].Close)

 
    def EveryMarketOpen(self):
        """ 
        Lookback length to determine last high and assess breakout status determined dynamically.
        Places market order if breakout determined to be present. If positions already open, stop risk
        values used to determine if fall in progress. Position close values (Stop market order) updated
        accordingly.
        """
        
        # Lookback length updated based on 30 day volatility (std of close history)
        close = self.History(self.symbol, 31, Resolution.Daily)["close"]
        todayvol = np.std(close[1:31])
        yesterdayvol = np.std(close[0:30])
        deltavol = (todayvol - yesterdayvol) / todayvol
        self.lookback = round(self.lookback * (1 + deltavol))
        
        # Ensure lookback remains in previously established bounds
        if self.lookback > self.ceiling:
            self.lookback = self.ceiling
        elif self.lookback < self.floor:
            self.lookback = self.floor
        
        # Establish historical highs for period of lookback
        self.high = self.History(self.symbol, self.lookback, Resolution.Daily)["high"]
        
        # Purchase if conditions met (no existing positions and breakout in progress)
        if not self.Securities[self.symbol].Invested and \
                self.Securities[self.symbol].Close >= max(self.high[:-1]):
            self.SetHoldings(self.symbol, 1)
            self.breakoutlvl = max(self.high[:-1])
            self.highestPrice = self.breakoutlvl
        
        
        # Once invested, create stop market order
        if self.Securities[self.symbol].Invested:
            
            # Stop market order based on previous stop risk level and degree of breakout
            if not self.Transactions.GetOpenOrders(self.symbol):
                self.stopMarketTicket = self.StopMarketOrder(self.symbol, \
                                        -self.Portfolio[self.symbol].Quantity, \
                                        self.initialStopRisk * self.breakoutlvl)
            
            
            # Check conditions to determine if stop market price should be updated 
            # If assets price higher than closing high and trailing stop price not below initial stop price
            if self.Securities[self.symbol].Close > self.highestPrice and \
                    self.initialStopRisk * self.breakoutlvl < self.Securities[self.symbol].Close * self.trailingStopRisk:
                
                # Reassign high price with closing price
                self.highestPrice = self.Securities[self.symbol].Close
                
                # Update stop market price (price stock exceeds before being sold)
                updateFields = UpdateOrderFields()
                updateFields.StopPrice = self.Securities[self.symbol].Close * self.trailingStopRisk
                self.stopMarketTicket.Update(updateFields)
                
                # Debug required to print in accordance with API
                self.Debug(updateFields.StopPrice)
            
            # Plot stop market prices over time
            self.Plot("Data Chart", "Stop Price", self.stopMarketTicket.Get(OrderField.StopPrice))
            
