# backtestr/portfolio/portfolio.py
class Portfolio:
    def __init__(self, cash=100_000.0):
        self.cash = float(cash)
        self.pos = {}  # symbol -> {"qty": int, "avg": float}
        self.equity_history = []
        self.trade_history = []  # Track all trades
        self.daily_pnl = []  # Track daily P&L

    def apply_fill(self, symbol, qty, price):
        lot = self.pos.get(symbol, {"qty": 0, "avg": 0.0})
        new_qty = lot["qty"] + qty

        # update avg cost when adding; keep avg when reducing
        if lot["qty"] == 0 and qty != 0:
            new_avg = price
        elif qty > 0 and new_qty != 0:
            new_avg = (lot["avg"] * lot["qty"] + price * qty) / new_qty
        else:
            new_avg = lot["avg"]

        self.cash -= price * qty
        if new_qty == 0:
            self.pos.pop(symbol, None)
        else:
            self.pos[symbol] = {"qty": new_qty, "avg": new_avg}
        
        # Log the trade
        trade_type = "BUY" if qty > 0 else "SELL"
        self.trade_history.append({
            "timestamp": getattr(self, '_current_timestamp', None),
            "symbol": symbol,
            "type": trade_type,
            "quantity": abs(qty),
            "price": price,
            "total_value": abs(qty * price),
            "cash_after": self.cash
        })

    def mark_to_market(self, prices: dict, ts):
        equity = self.cash
        for sym, lot in self.pos.items():
            equity += lot["qty"] * prices[sym]
        
        # Calculate daily P&L
        if self.equity_history:
            prev_equity = self.equity_history[-1][1]
            daily_pnl = equity - prev_equity
            daily_pnl_pct = (daily_pnl / prev_equity) * 100 if prev_equity > 0 else 0
        else:
            daily_pnl = 0
            daily_pnl_pct = 0
        
        self.equity_history.append((ts, equity))
        self.daily_pnl.append((ts, daily_pnl, daily_pnl_pct))
        
        # Store timestamp for trade logging
        self._current_timestamp = ts
        
        return equity
