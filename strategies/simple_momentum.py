class SimpleMomentum:
    """
    Simple momentum strategy that buys when price is above moving average
    and sells when below
    """
    
    def __init__(self, symbol, lookback=20, threshold=0.02):
        """
        Initialize SimpleMomentum strategy.
        
        Args:
            symbol: Symbol to trade
            lookback: Lookback period for momentum calculation
            threshold: Momentum threshold for trading signals
        """
        self.symbol = symbol
        self.lookback = lookback
        self.threshold = threshold
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
        
        # Need enough data for momentum calculation
        if len(self.price_history) < self.lookback + 1:
            return
        
        # Calculate momentum (price change over lookback period)
        old_price = self.price_history[-self.lookback - 1]
        momentum = (current_price - old_price) / old_price
        
        # Get current position
        position = ctx.position(self.symbol)
        current_qty = position["qty"] if position else 0
        
        # Strategy logic
        if momentum > self.threshold and current_qty == 0:
            # Strong positive momentum - buy signal
            target_qty = int((ctx.cash * 0.95) // current_price)
            if target_qty > 0:
                ctx.order_market(self.symbol, target_qty)
                print(f"📈 Momentum BUY: {target_qty} shares @ ${current_price:.2f} (momentum: {momentum*100:.1f}%)")
                
        elif momentum < -self.threshold and current_qty > 0:
            # Strong negative momentum - sell signal
            ctx.order_market(self.symbol, -current_qty)
            print(f"📉 Momentum SELL: {current_qty} shares @ ${current_price:.2f} (momentum: {momentum*100:.1f}%)")
