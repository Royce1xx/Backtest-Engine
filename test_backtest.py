#!/usr/bin/env python3
"""
Simple test script for the backtest engine
"""

try:
    from data.loader import load_symbols
    from engine.clock import Clock
    from engine.engine import Engine
    from engine.context import Context
    from portfolio.portfolio import Portfolio
    from strategies.buy_and_hold import BuyAndHold
    
    print("✓ All imports successful!")
    
    # Test data loading
    symbols = ["AAPL"]
    data, timeline = load_symbols({"AAPL": "data/AAPL_2022.csv"})
    print(f"✓ Data loaded: {len(timeline)} data points")
    
    # Test components
    clock = Clock(timeline)
    port = Portfolio(cash=100_000)
    eng = Engine(data, timeline, symbols, port)
    strat = BuyAndHold(symbol="AAPL", cash_fraction=0.95)
    
    print("✓ All components initialized!")
    
    # Run backtest
    print("\nRunning backtest...")
    equity_hist = eng.run(strat, Context, clock)
    
    # Results
    initial_equity = equity_hist[0][1]
    final_equity = equity_hist[-1][1]
    total_return = final_equity - initial_equity
    percent_return = (total_return / initial_equity) * 100
    
    print(f"\n=== BACKTEST RESULTS ===")
    print(f"Initial Capital: ${initial_equity:,.2f}")
    print(f"Final Equity: ${final_equity:,.2f}")
    print(f"Total Return: ${total_return:,.2f}")
    print(f"Percent Return: {percent_return:.2f}%")
    
    print(f"\n=== FINAL PORTFOLIO ===")
    print(f"Cash: ${port.cash:,.2f}")
    for symbol, position in port.pos.items():
        print(f"{symbol}: {position['qty']} shares @ ${position['avg']:.2f} avg")
    
    print("\n✓ Backtest completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
