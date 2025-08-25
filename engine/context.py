# backtestr/engine/context.py
import pandas as pd

class Context:
    """
    Provides an interface for strategies to interact with the engine.
    Gives strategies access to market data, portfolio state, and order submission.
    """
    
    def __init__(self, data, portfolio, execution_model):
        """
        Initialize the context.
        
        Args:
            data: dict {symbol: DataFrame} or DataFrame for single symbol
            portfolio: Portfolio instance
            execution_model: ExecutionModel instance
        """
        self.data = data
        self.portfolio = portfolio
        self.execution_model = execution_model
        self.current_timestamp = None  # Current time in backtest
        
        # Handle single symbol data (from yfinance)
        if isinstance(data, pd.DataFrame):
            self.symbols = ["data"]
            self.data = {"data": data}
        else:
            self.symbols = list(data.keys())
    
    def price(self, symbol):
        """
        Get the current price for a symbol.
        
        Args:
            symbol: Symbol to get price for
            
        Returns:
            float: Current close price
        """
        # For yfinance data, we use "data" as the key
        data_key = "data"
        if data_key not in self.data:
            return None
        
        df = self.data[data_key]
        if self.current_timestamp is None:
            return None
        
        # Find the current bar
        current_bar = df[df['timestamp'] == self.current_timestamp]
        if current_bar.empty:
            return None
        
        return float(current_bar.iloc[0]['close'])
    
    def position(self, symbol):
        """
        Get current position for a symbol.
        
        Args:
            symbol: Symbol to get position for
            
        Returns:
            dict: Position info with 'qty' and 'avg' keys
        """
        return self.portfolio.positions.get(symbol, {"qty": 0, "avg": 0})
    
    @property
    def cash(self):
        """Get current cash balance."""
        return self.portfolio.cash
    
    def order_market(self, symbol, qty):
        """
        Submit a market order.
        
        Args:
            symbol: Symbol to trade
            qty: Quantity (positive for buy, negative for sell)
        """
        current_price = self.price(symbol)
        if current_price is None:
            print(f"❌ No price data for {symbol} at {self.current_timestamp}")
            return
        
        # Create and execute the order
        from execution.order import Order
        order = Order(symbol=symbol, qty=qty, type="market")
        
        # Simulate immediate fill at current price
        fill_price = current_price
        self.portfolio.apply_fill(symbol, qty, fill_price)
        
        print(f"📊 Market order executed: {qty} {symbol} @ ${fill_price:.2f}")
    
    def order_limit(self, symbol, qty, limit_price):
        """
        Submit a limit order.
        
        Args:
            symbol: Symbol to trade
            qty: Quantity (positive for buy, negative for sell)
            limit_price: Limit price for the order
        """
        current_price = self.price(symbol)
        if current_price is None:
            print(f"❌ No price data for {symbol} at {self.current_timestamp}")
            return
        
        # Check if limit order can be filled
        if (qty > 0 and current_price <= limit_price) or (qty < 0 and current_price >= limit_price):
            # Limit order can be filled
            self.portfolio.apply_fill(symbol, qty, limit_price)
            print(f"📊 Limit order filled: {qty} {symbol} @ ${limit_price:.2f}")
        else:
            print(f"⏳ Limit order pending: {qty} {symbol} @ ${limit_price:.2f} (current: ${current_price:.2f})")
