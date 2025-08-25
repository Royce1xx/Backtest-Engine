#!/usr/bin/env python3
"""
Compare multiple trading strategies on the same data
"""

from data.loader import load_symbols
from engine.clock import Clock
from engine.engine import Engine
from engine.context import Context
from portfolio.portfolio import Portfolio
from strategies.buy_and_hold import BuyAndHold
from strategies.simple_momentum import SimpleMomentum

def run_strategy(strategy_name, strategy_class, **kwargs):
    """Run a single strategy and return results"""
    print(f"\n{'='*50}")
    print(f"Running {strategy_name} Strategy")
    print(f"{'='*50}")
    
    # Initialize components
    symbols = ["AAPL"]
    data, timeline = load_symbols({"AAPL": "data/AAPL_2022.csv"})
    clock = Clock(timeline)
    port = Portfolio(cash=100_000)
    eng = Engine(data, timeline, symbols, port)
    
    # Create strategy instance
    if strategy_name == "Buy and Hold":
        strat = strategy_class(symbol="AAPL", cash_fraction=0.95)
    else:
        strat = strategy_class(symbol="AAPL", lookback=20, cash_fraction=0.95)
    
    # Run backtest
    equity_hist = eng.run(strat, Context, clock)
    
    # Calculate results
    initial_equity = equity_hist[0][1]
    final_equity = equity_hist[-1][1]
    total_return = final_equity - initial_equity
    percent_return = (total_return / initial_equity) * 100
    
    # Calculate max drawdown
    peak = initial_equity
    max_drawdown = 0
    for _, equity in equity_hist:
        if equity > peak:
            peak = equity
        drawdown = (peak - equity) / peak * 100
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    results = {
        'strategy': strategy_name,
        'initial': initial_equity,
        'final': final_equity,
        'return': total_return,
        'return_pct': percent_return,
        'max_drawdown': max_drawdown,
        'final_cash': port.cash,
        'final_position': port.pos.get('AAPL', {'qty': 0, 'avg': 0})
    }
    
    # Print results
    print(f"Initial Capital: ${initial_equity:,.2f}")
    print(f"Final Equity: ${final_equity:,.2f}")
    print(f"Total Return: ${total_return:,.2f}")
    print(f"Percent Return: {percent_return:.2f}%")
    print(f"Max Drawdown: {max_drawdown:.2f}%")
    print(f"Final Cash: ${port.cash:,.2f}")
    if port.pos.get('AAPL'):
        pos = port.pos['AAPL']
        print(f"AAPL Position: {pos['qty']} shares @ ${pos['avg']:.2f} avg")
    else:
        print("AAPL Position: No position")
    
    return results

def main():
    print("🚀 ELITE BACKTEST ENGINE - STRATEGY COMPARISON")
    print("Testing strategies on AAPL 2022 data with $100,000 initial capital")
    
    # Define strategies to test
    strategies = [
        ("Buy and Hold", BuyAndHold),
        ("Simple Momentum", SimpleMomentum)
    ]
    
    all_results = []
    
    for strategy_name, strategy_class in strategies:
        try:
            results = run_strategy(strategy_name, strategy_class)
            all_results.append(results)
        except Exception as e:
            print(f"❌ Error running {strategy_name}: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary comparison
    if all_results:
        print(f"\n{'='*80}")
        print("STRATEGY COMPARISON SUMMARY")
        print(f"{'='*80}")
        print(f"{'Strategy':<20} {'Return %':<12} {'Max DD %':<12} {'Final Equity':<15}")
        print(f"{'-'*80}")
        
        for result in all_results:
            print(f"{result['strategy']:<20} {result['return_pct']:>10.2f}% {result['max_drawdown']:>10.2f}% ${result['final']:>13,.2f}")
        
        # Find best performer
        best = max(all_results, key=lambda x: x['return_pct'])
        print(f"\n🏆 Best Performer: {best['strategy']} with {best['return_pct']:.2f}% return")
        
        # Find lowest drawdown
        lowest_dd = min(all_results, key=lambda x: x['max_drawdown'])
        print(f"🛡️  Lowest Drawdown: {lowest_dd['strategy']} with {lowest_dd['max_drawdown']:.2f}% max drawdown")

if __name__ == "__main__":
    main()
