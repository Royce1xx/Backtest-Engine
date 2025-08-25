import pandas as pd
from execution.order import Order
from execution.fills import ExecutionModel
from portfolio.portfolio import Portfolio
from engine.clock import Clock
from engine.context import Context

class Engine:
    """
    Main backtest engine that orchestrates the entire simulation.
    Coordinates data, portfolio, and strategy execution.
    """
    
    def __init__(self, data, timeline, portfolio, execution_model):
        """
        Initialize the engine.
        
        Args:
            data: dict {symbol: DataFrame} or DataFrame for single symbol
            timeline: list of timestamps to iterate through
            portfolio: Portfolio instance
            execution_model: ExecutionModel instance
        """
        self.data = data
        self.timeline = timeline
        self.portfolio = portfolio
        self.execution_model = execution_model
        self.clock = Clock(timeline)  # Time management
        self.context = Context(self.data, self.portfolio, self.execution_model)  # Strategy interface
        
        # Handle single symbol data (from yfinance)
        if isinstance(data, pd.DataFrame):
            self.symbols = ["data"]
            self.data = {"data": data}
        else:
            self.symbols = list(data.keys())
    
    def run(self, strategy):
        """
        Run the backtest with the given strategy.
        
        Args:
            strategy: Strategy instance with on_bar method
        """
        print(f"🚀 Starting backtest for {len(self.timeline)} time periods...")
        
        for ts in self.clock:  # Iterate through each timestamp
            # Update portfolio mark-to-market
            self.portfolio.mark_to_market(ts, self.data)
            
            # Update context with current timestamp
            self.context.current_timestamp = ts
            
            # Execute strategy logic
            strategy.on_bar(self.context)
            
            # Process any pending orders
            self._process_orders(ts)
        
        print(f"✅ Backtest completed!")
    
    def _process_orders(self, timestamp):
        """
        Process any pending orders at the given timestamp.
        """
        # This is a simplified version - in a real engine you'd have order management
        pass
