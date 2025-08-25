# backtestr/run.py
from data.loader import load_symbols
from engine.clock import Clock
from engine.engine import Engine
from engine.context import Context
from portfolio.portfolio import Portfolio
from strategies.buy_and_hold import BuyAndHold

if __name__ == "__main__":
    symbols = ["AAPL"]
    data, timeline = load_symbols({"AAPL": "data/AAPL_2022.csv"})
    clock = Clock(timeline)
    port = Portfolio(cash=100_000)
    eng = Engine(data, timeline, symbols, port)
    strat = BuyAndHold(symbol="AAPL", cash_fraction=0.95)
    
    print("Starting backtest with $100,000 initial capital...")
    print(f"Data points: {len(timeline)}")
    print(f"Date range: {timeline[0]} to {timeline[-1]}")
    
    equity_hist = eng.run(strat, Context, clock)
    
    # Calculate results
    initial_equity = equity_hist[0][1]
    final_equity = equity_hist[-1][1]
    total_return = final_equity - initial_equity
    percent_return = (total_return / initial_equity) * 100
    
    print(f"\n=== BACKTEST RESULTS ===")
    print(f"Initial Capital: ${initial_equity:,.2f}")
    print(f"Final Equity: ${final_equity:,.2f}")
    print(f"Total Return: ${total_return:,.2f}")
    print(f"Percent Return: {percent_return:.2f}%")
    
    # Show final portfolio state
    print(f"\n=== FINAL PORTFOLIO ===")
    print(f"Cash: ${port.cash:,.2f}")
    for symbol, position in port.pos.items():
        print(f"{symbol}: {position['qty']} shares @ ${position['avg']:.2f} avg")
