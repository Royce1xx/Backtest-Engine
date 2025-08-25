# backtestr/execution/fills.py
from .order import Order

class ExecutionModel:
    """
    Simulates order execution with slippage and fees.
    Handles market and limit order fills.
    """
    
    def __init__(self, slippage=0.001, commission=0.005):
        """
        Initialize execution model.
        
        Args:
            slippage: Price slippage as fraction (0.001 = 0.1%)
            commission: Commission as fraction (0.005 = 0.5%)
        """
        self.slippage = slippage
        self.commission = commission
    
    def fill(self, orders, current_prices):
        """
        Simulate order fills.
        
        Args:
            orders: List of Order objects
            current_prices: Dict of current prices by symbol
            
        Returns:
            tuple: (fills, total_fees)
        """
        fills = []
        total_fees = 0
        
        for order in orders:
            if order.symbol in current_prices:
                # Get current price
                current_price = current_prices[order.symbol]["close"]
                
                # Apply slippage
                if order.type == "market":
                    # Market orders get filled at current price with slippage
                    fill_price = current_price * (1 + self.slippage) if order.qty > 0 else current_price * (1 - self.slippage)
                else:
                    # Limit orders get filled at limit price
                    fill_price = order.limit_price
                
                # Calculate fees
                fees = abs(order.qty * fill_price * self.commission)
                total_fees += fees
                
                # Record fill
                fills.append((order.symbol, order.qty, fill_price))
        
        return fills, total_fees
