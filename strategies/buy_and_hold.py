class DynamicTrader:
    """
    Dynamic trading strategy with profit targets and stop losses.
    Buys when cash available, sells at profit target or stop loss, then re-enters.
    """
    
    def __init__(self, symbol, cash_fraction=0.95, profit_target=0.15, stop_loss=0.08):
        self.symbol = symbol
        self.cash_fraction = cash_fraction  # Fraction of cash to use
        self.profit_target = profit_target  # 15% profit target
        self.stop_loss = stop_loss         # 8% stop loss
        self.position = None  # Track current position
        self.entry_price = 0  # Track entry price
        self.trade_count = 0  # Count total trades

    def on_bar(self, ctx):
        current_price = ctx.price(self.symbol)
        position = ctx.position(self.symbol)

        # If we have no position, look to buy
        if not position or position["qty"] == 0:
            if ctx.cash > 1000:  # Only buy if we have enough cash
                target_qty = int((ctx.cash * self.cash_fraction) // current_price)
                if target_qty > 0:
                    ctx.order_market(self.symbol, target_qty)
                    self.entry_price = current_price
                    self.trade_count += 1
                    print(f"🟢 BUY #{self.trade_count}: {target_qty} shares at ${current_price:.2f}")

        # If we have a position, check for exit conditions
        elif position and position["qty"] > 0:
            entry_price = position["avg"]
            current_pnl_pct = (current_price - entry_price) / entry_price

            # Check profit target
            if current_pnl_pct >= self.profit_target:
                ctx.order_market(self.symbol, -position["qty"])  # Sell all
                print(f"🟡 PROFIT TARGET HIT: Sold {position['qty']} shares at ${current_price:.2f} (+{current_pnl_pct*100:.1f}%)")
                self.trade_count += 1

            # Check stop loss
            elif current_pnl_pct <= -self.stop_loss:
                ctx.order_market(self.symbol, -position["qty"])  # Sell all
                print(f"🔴 STOP LOSS HIT: Sold {position['qty']} shares at ${current_price:.2f} ({current_pnl_pct*100:.1f}%)")
                self.trade_count += 1
