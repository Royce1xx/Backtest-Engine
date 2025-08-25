class SimpleMomentum:
    """
    Simple momentum strategy that buys when price is above moving average
    and sells when below
    """
    def __init__(self, symbol, lookback=20, cash_fraction=0.95):
        self.symbol = symbol
        self.lookback = lookback
        self.cash_fraction = cash_fraction
        self.position = 0

    def on_bar(self, ctx):
        bars = ctx.bars(self.symbol, n=self.lookback + 1)
        if len(bars) < self.lookback:
            return
            
        current_price = ctx.price(self.symbol)
        moving_avg = bars["close"].tail(self.lookback).mean()
        
        # Simple momentum signal
        if current_price > moving_avg and self.position == 0:
            # Buy signal
            target_qty = int((ctx.cash * self.cash_fraction) // current_price)
            if target_qty > 0:
                ctx.order_market(self.symbol, target_qty)
                self.position = target_qty
                
        elif current_price < moving_avg and self.position > 0:
            # Sell signal
            ctx.order_market(self.symbol, -self.position)
            self.position = 0
