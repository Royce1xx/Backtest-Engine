# backtestr/strategies/macross.py
class MACross:
    """
    Moving Average Crossover Strategy
    """
    
    def __init__(self, symbol, short_window=10, long_window=30, risk_frac=0.95):
        """
        Initialize MACross strategy.
        
        Args:
            symbol: Symbol to trade
            short_window: Short moving average period
            long_window: Long moving average period
            risk_frac: Fraction of cash to risk
        """
        self.symbol = symbol
        self.short_window = short_window
        self.long_window = long_window
        self.risk_frac = risk_frac
        self.price_history = []
    
    def on_bar(self, ctx):
        """
        Execute strategy logic on each bar.
        
        Args:
            ctx: Context object providing market data and portfolio access
        """
        current_price = ctx.price(self.symbol)
        if current_price is None:
            return
        
        # Add current price to history
        self.price_history.append(current_price)
        
        # Need enough data for moving averages
        if len(self.price_history) < self.long_window:
            return
        
        # Calculate moving averages
        short_ma = sum(self.price_history[-self.short_window:]) / self.short_window
        long_ma = sum(self.price_history[-self.long_window:]) / self.long_window
        
        # Get current position
        position = ctx.position(self.symbol)
        current_qty = position["qty"] if position else 0
        
        # Strategy logic: buy when short MA > long MA
        target_qty = 0
        if short_ma > long_ma:
            # Bullish signal - calculate target position
            target_qty = int((ctx.cash * self.risk_frac) // current_price)
        
        # Calculate order quantity
        order_qty = target_qty - current_qty
        
        # Execute order if needed
        if order_qty > 0:
            # Buy
            ctx.order_market(self.symbol, order_qty)
        elif order_qty < 0:
            # Sell
            ctx.order_market(self.symbol, order_qty)
