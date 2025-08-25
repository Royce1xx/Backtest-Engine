# backtestr/execution/orders.py
from dataclasses import dataclass

@dataclass
class Order:
    """
    Represents a trading order.
    Contains symbol, quantity, order type, and optional limit price.
    """
    symbol: str      # Stock symbol to trade
    qty: int         # Quantity (positive = buy, negative = sell)
    type: str        # Order type: "market" or "limit"
    limit_price: float = None  # Limit price for limit orders
