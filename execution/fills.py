# backtestr/execution/fills.py
from .order import Order

class ExecutionModel:
    def __init__(self, slippage_bps=0, fee_rate=0.0):
        self.slippage_bps = slippage_bps
        self.fee_rate = fee_rate

    def _slip(self, price, side):
        slip = price * (self.slippage_bps / 10_000.0)
        return price + slip if side > 0 else price - slip

    def fill(self, orders: list[Order], bar_by_sym: dict):
        fills = []
        fees = 0.0
        for o in orders:
            bar = bar_by_sym[o.symbol]
            if o.type == "market":
                px = self._slip(float(bar["open"]), o.qty)
                fills.append((o.symbol, o.qty, px))
                fees += abs(px * o.qty) * self.fee_rate
            elif o.type == "limit":
                if bar["low"] <= o.limit_price <= bar["high"]:
                    px = float(o.limit_price)
                    fills.append((o.symbol, o.qty, px))
                    fees += abs(px * o.qty) * self.fee_rate
        return fills, fees
