# backtestr/engine/engine.py
from execution.order import Order
from execution.fills import ExecutionModel

class Engine:
    def __init__(self, data, timeline, symbols, portfolio, exec_model=None):
        self.data = data
        self.timeline = timeline
        self.symbols = symbols
        self.portfolio = portfolio
        self.exec = exec_model or ExecutionModel()
        self._row = {s: 0 for s in symbols}
        self.state = {"bars": {}, "history": {s: self.data[s].copy() for s in symbols}}
        self._now = None
        self._order_buf = []

    def _submit_order(self, od):
        self._order_buf.append(od)

    def _advance_bar(self, sym, ts):
        df = self.data[sym]
        i = self._row[sym]
        if i < len(df) and df.iloc[i]["timestamp"] == ts:
            self.state["bars"][sym] = df.iloc[i]
            self._row[sym] += 1

    def run(self, strategy, context_cls, clock):
        def now_callable(): return self._now
        ctx = context_cls(self.symbols, self.state, self.portfolio, self._submit_order, now_callable)

        while clock.has_next():
            ts = clock.next()
            self._now = ts

            # advance all symbols to this timestamp
            bar_by_sym = {}
            for s in self.symbols:
                self._advance_bar(s, ts)
                if s in self.state["bars"]:
                    b = self.state["bars"][s]
                    bar_by_sym[s] = {
                        "open": b["open"], "high": b["high"],
                        "low": b["low"], "close": b["close"],
                        "volume": b["volume"]
                    }

            # strategy step
            self._order_buf.clear()
            strategy.on_bar(ctx)

            # translate orders → fills → portfolio
            orders = [Order(symbol=o["symbol"], qty=o["qty"], type=o["type"], limit_price=o.get("limit_price"))
                      for o in self._order_buf]
            fills, fees = self.exec.fill(orders, bar_by_sym)
            for sym, qty, px in fills:
                self.portfolio.apply_fill(sym, qty, px)
            self.portfolio.cash -= fees

            # mark to market
            last_prices = {s: float(bar_by_sym[s]["close"]) for s in bar_by_sym}
            self.portfolio.mark_to_market(last_prices, ts)

        return self.portfolio.equity_history
