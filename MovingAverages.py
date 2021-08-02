class MovingAverages(QCAlgorithm):
    """
    Rule based trading strategy.
    
    200-50 moving average algorithm. 
    Purchases equity when 50 day average higher than 200 day average.
    Positions closed when conditions no longer met.
    """
    
    def Initialize(self):
        """Initializes base conditions: date for backtesting, purchase frequency, coarse data."""
        
        # Data Resolution
        self.SetStartDate(2011, 1, 7)
        self.SetEndDate(2015, 1, 7)
        self.SetCash(100000)
        
        # Universe selection model
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction) 
        self.averages = { }
    
    
    def CoarseSelectionFunction(self, universe):  
        """
        Filters data using predefined methods. Composes return list with all possible positions 
        in accordance with predefnied constraints. Returns set with 10 positions.
        """
         
        # Data filtering method
        selected = []
        universe = sorted(universe, key=lambda c: c.DollarVolume, reverse=True)  
        universe = [c for c in universe if c.Price > 10][:100]

        # History called to compensate for first initialization
        for coarse in universe:  
            symbol = coarse.Symbol
            
            if symbol not in self.averages:
                history = self.History(symbol, 200, Resolution.Daily)
                self.averages[symbol] = SelectionData(history) 

            self.averages[symbol].update(self.Time, coarse.AdjustedPrice)
            
            # Base requirements met to add data
            if  self.averages[symbol].is_ready() and self.averages[symbol].fast > self.averages[symbol].slow:
                selected.append(symbol)
        
        return selected[:10]
      
        
    def OnSecuritiesChanged(self, changes):
        """
        Reviews parameter changes, definining current holdings.
        Closes and opens appropriate positions in regard to aformentioned argument.
        
        """
        
        # Closes positions
        for security in changes.RemovedSecurities:
            self.Liquidate(security.Symbol)
       
       # Opens Positions
        for security in changes.AddedSecurities:
            self.SetHoldings(security.Symbol, 0.10)
            
            
class SelectionData():
    """
    Main methods for finding data and determining whether data is ready.
    
    Defines method of 200 and 50 day averages. 
    Determines if enough data is present for model to work.
    Updates moving averages.
    """
    
    def __init__(self, history):
        """ 
        Initializes slow and fast averages defined as 200 and 50 day averages respectively.
        When instantiated, data drawn from history. Stored during the pass moving forward.
        """
        
        # Set moving averages for 200 days and 50 days
        self.slow = ExponentialMovingAverage(200)
        self.fast = ExponentialMovingAverage(50)
        
        # Loop over the history data and update the indicators
        for bar in history.itertuples():
            self.fast.Update(bar.Index[1], bar.close)
            self.slow.Update(bar.Index[1], bar.close)
    
    
    def is_ready(self):
        """ Returns boolean with status of moving average values."""
        return self.slow.IsReady and self.fast.IsReady
    
    
    def update(self, time, price):
        """ Updates fast and slow moving average values."""
        self.fast.Update(time, price)
        self.slow.Update(time, price)
 
