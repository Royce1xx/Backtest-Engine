# backtestr/engine/context.py
class Context:
    def __init__(self, symbols, state, portfolio, submit_order, now_callable):
        self.symbols = symbols
        self._state = state
        self._portfolio = portfolio
        self._submit = submit_order
        self._now = now_callable

    @property
    def now(self):
        return self._now()

    def price(self, symbol):
        return float(self._state["bars"][symbol]["close"])

    def bars(self, symbol, n):
        return self._state["history"][symbol].tail(n)

    def position(self, symbol):
        return self._portfolio.pos.get(symbol)

    @property
    def cash(self):
        return self._portfolio.cash

    def order_market(self, symbol, qty):
        self._submit({"type": "market", "symbol": symbol, "qty": qty})

    def order_limit(self, symbol, qty, px):
        self._submit({"type": "limit", "symbol": symbol, "qty": qty, "limit_price": px})
