# backtestr/execution/orders.py
from dataclasses import dataclass

@dataclass
class Order:
    symbol: str
    qty: int                  # +buy / -sell
    type: str = "market"      # "market" or "limit"
    limit_price: float | None = None
