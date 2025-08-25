import pandas as pd

class Portfolio:
    """
    Manages cash, positions, and tracks equity over time.
    """
    
    def __init__(self, initial_cash):
        """
        Initialize portfolio with starting cash.
        
        Args:
            initial_cash: Starting cash amount
        """
        self.cash = initial_cash
        self.positions = {}  # symbol -> {"qty": int, "avg": float}
        self.equity_history = [(None, initial_cash)]  # (timestamp, equity)
        self.trade_history = []
        self.daily_pnl = []
    
    def apply_fill(self, symbol, qty, price):
        """
        Apply a trade fill to the portfolio.
        
        Args:
            symbol: Symbol being traded
            qty: Quantity (positive for buy, negative for sell)
            price: Fill price
        """
        if qty == 0:
            return
        
        # Calculate total value
        total_value = abs(qty * price)
        
        # Update cash
        if qty > 0:  # Buy
            self.cash -= total_value
        else:  # Sell
            self.cash += total_value
        
        # Update position
        if symbol not in self.positions:
            self.positions[symbol] = {"qty": 0, "avg": 0}
        
        pos = self.positions[symbol]
        old_qty = pos["qty"]
        old_avg = pos["avg"]
        
        if qty > 0:  # Buy
            if old_qty >= 0:  # Adding to long position
                new_qty = old_qty + qty
                new_avg = ((old_qty * old_avg) + (qty * price)) / new_qty if new_qty > 0 else 0
            else:  # Covering short position
                new_qty = old_qty + qty
                if new_qty >= 0:  # Now long
                    new_avg = price
                else:  # Still short
                    new_avg = old_avg
        else:  # Sell
            if old_qty > 0:  # Reducing long position
                new_qty = old_qty + qty
                new_avg = old_avg
            else:  # Adding to short position
                new_qty = old_qty + qty
                new_avg = price
        
        pos["qty"] = new_qty
        pos["avg"] = new_avg
        
        # Clean up zero positions
        if new_qty == 0:
            del self.positions[symbol]
        
        # Log the trade
        trade_type = "BUY" if qty > 0 else "SELL"
        self.trade_history.append({
            "timestamp": getattr(self, '_current_timestamp', None),
            "symbol": symbol,
            "type": trade_type,
            "quantity": abs(qty),
            "price": price,
            "total_value": total_value,
            "cash_after": self.cash
        })
    
    def mark_to_market(self, timestamp, data):
        """
        Mark portfolio to market at current prices.
        
        Args:
            timestamp: Current timestamp
            data: dict {symbol: DataFrame} or DataFrame for single symbol
        """
        # Handle single symbol data (from yfinance)
        if isinstance(data, pd.DataFrame):
            symbols = ["data"]
            data = {"data": data}
        else:
            symbols = list(data.keys())
        
        # Calculate current equity
        equity = self.cash
        
        for symbol in symbols:
            if symbol in self.positions and self.positions[symbol]["qty"] != 0:
                # Get current price for this symbol
                df = data[symbol]
                current_bar = df[df['timestamp'] == timestamp]
                
                if not current_bar.empty:
                    current_price = float(current_bar.iloc[0]['close'])
                    position_value = self.positions[symbol]["qty"] * current_price
                    equity += position_value
        
        # Calculate daily P&L
        if self.equity_history:
            prev_equity = self.equity_history[-1][1]
            daily_pnl = equity - prev_equity
            daily_pnl_pct = (daily_pnl / prev_equity) * 100 if prev_equity > 0 else 0
        else:
            daily_pnl = 0
            daily_pnl_pct = 0
        
        self.equity_history.append((timestamp, equity))
        self.daily_pnl.append((timestamp, daily_pnl, daily_pnl_pct))
        
        # Store timestamp for trade logging
        self._current_timestamp = timestamp
    
    def get_current_equity(self):
        """Get current portfolio equity."""
        if self.equity_history:
            return self.equity_history[-1][1]
        return self.cash
    
    def get_total_return(self):
        """Get total return since inception."""
        if len(self.equity_history) < 2:
            return 0
        
        initial = self.equity_history[0][1]
        current = self.equity_history[-1][1]
        return current - initial
    
    def get_total_return_pct(self):
        """Get total return percentage since inception."""
        if len(self.equity_history) < 2:
            return 0
        
        initial = self.equity_history[0][1]
        current = self.equity_history[-1][1]
        return ((current - initial) / initial) * 100 if initial > 0 else 0
