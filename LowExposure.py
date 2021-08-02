# In progress

import numpy as np

class LowExposure(QCAlgorithm):

    def Initialize(self):
        
        self.SetCash(100000)
        
        # Initialize start and end date
        self.SetStartDate(2015, 1, 7)
        self.SetEndDate(2019, 1, 7)
        
        self.symbol = self.AddEquity("Spy", Resolution.Daily).Symbol
        
        self.lookback = 7
        
        self.Schedule.On(self.DateRules.EveryDay(self.symbol), \
                        self.TimeRules.AfterMarketOpen(self.symbol, 20), \
                        Action(self.EveryMarketOpen))
        
        # self.initialStopRisk = 0.98
        # self.trailingStopRisk = 0.9
        
        
    def onData(self, data):
        self.Plot("Data Chart", self.symbol, self.Securities[self.symbol].Close)
        
        
    def EveryMarketOpen(self):
        self.high = self.History(self.symbol, 7, Resolution.Daily)['high']
        self.low = self.History(self.symbol, 7, Resolution.Daily)['low']
        self.moving_avg = self.SMA(self.symbol, 200, Resolution.Daily)
        # change ema to sma
        
        if self.moving_avg and not self.Securities[self.symbol].Invested and \
                self.Securities[self.symbol].Close < min(self.low) and \
                self.Securities[self.symbol].Close >= self.moving_avg:
            self.SetHoldings(self.symbol, 1)
            
        if self.Securities[self.symbol].Invested:
            if not self.Transactions.GetOpenOrders(self.symbol):
                self.stopMarketTicket = self.StopMarketOrder(self.symbol, \
                                        -self.Portfolio[self.symbol].Quantity, \
                                        max(self.high))
             
            updateFields = UpdateOrderFields()
            updateFields.StopPrice = max(self.high)
            self.stopMarketTicket.Update(updateFields)
            
            self.Debug(updateFields.StopPrice)
        
        self.Plot("Data Chart", "Stop Price", self.stopMarketTicket.Get(OrderField.StopPrice))
        
