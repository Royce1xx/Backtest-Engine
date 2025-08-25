#!/usr/bin/env python3
"""
Detailed backtest script showing comprehensive trading information
"""

from data.loader import load_symbols
from engine.clock import Clock
from engine.engine import Engine
from engine.context import Context
from portfolio.portfolio import Portfolio
from strategies.buy_and_hold import DynamicTrader

def format_currency(amount):
    """Format amount as currency"""
    return f"${amount:,.2f}"

def format_percentage(amount):
    """Format amount as percentage"""
    return f"{amount:+.2f}%"

def main():
    print("🚀 ELITE BACKTEST ENGINE - DYNAMIC TRADING ANALYSIS")
    print("=" * 60)
    
    # Initialize components
    symbols = ["AAPL"]
    data, timeline = load_symbols({"AAPL": "data/AAPL_2022.csv"})
    clock = Clock(timeline)
    port = Portfolio(cash=100_000)
    eng = Engine(data, timeline, symbols, port)
    strat = DynamicTrader(symbol="AAPL", cash_fraction=0.95, profit_target=0.15, stop_loss=0.08)
    
    print(f"Starting Capital: {format_currency(port.cash)}")
    print(f"Data Points: {len(timeline)}")
    print(f"Date Range: {timeline[0].strftime('%Y-%m-%d')} to {timeline[-1].strftime('%Y-%m-%d')}")
    print()
    
    # Run backtest
    print("Running backtest...")
    equity_hist = eng.run(strat, Context, clock)
    
    # ===== TRADE SUMMARY =====
    print("\n" + "=" * 60)
    print("📊 TRADE SUMMARY")
    print("=" * 60)
    
    if port.trade_history:
        for i, trade in enumerate(port.trade_history, 1):
            print(f"Trade #{i}: {trade['type']} {trade['quantity']} shares of {trade['symbol']}")
            print(f"  Date: {trade['timestamp'].strftime('%Y-%m-%d') if trade['timestamp'] else 'N/A'}")
            print(f"  Price: {format_currency(trade['price'])}")
            print(f"  Total Value: {format_currency(trade['total_value'])}")
            print(f"  Cash After: {format_currency(trade['cash_after'])}")
            print()
    else:
        print("No trades executed")
    
    # ===== POSITION TRACKING =====
    print("=" * 60)
    print("📈 POSITION TRACKING")
    print("=" * 60)
    
    for symbol, position in port.pos.items():
        current_price = float(data[symbol].iloc[-1]["close"])
        position_value = position["qty"] * current_price
        unrealized_pnl = position_value - (position["qty"] * position["avg"])
        unrealized_pnl_pct = (unrealized_pnl / (position["qty"] * position["avg"])) * 100 if position["avg"] > 0 else 0
        
        print(f"Symbol: {symbol}")
        print(f"  Shares: {position['qty']:,}")
        print(f"  Average Cost: {format_currency(position['avg'])}")
        print(f"  Current Price: {format_currency(current_price)}")
        print(f"  Position Value: {format_currency(position_value)}")
        print(f"  Unrealized P&L: {format_currency(unrealized_pnl)} ({format_percentage(unrealized_pnl_pct)})")
        print()
    
    # ===== CASH FLOW ANALYSIS =====
    print("=" * 60)
    print("💰 CASH FLOW ANALYSIS")
    print("=" * 60)
    
    initial_cash = 100_000
    final_cash = port.cash
    total_invested = initial_cash - final_cash
    
    print(f"Initial Cash: {format_currency(initial_cash)}")
    print(f"Final Cash: {format_currency(final_cash)}")
    print(f"Total Invested: {format_currency(total_invested)}")
    print(f"Cash Utilization: {((total_invested / initial_cash) * 100):.1f}%")
    print()
    
    # ===== DAILY P&L ANALYSIS =====
    print("=" * 60)
    print("📅 DAILY P&L ANALYSIS")
    print("=" * 60)
    
    if port.daily_pnl:
        # Show first 10 days and last 10 days
        print("First 10 Days:")
        for i, (ts, pnl, pnl_pct) in enumerate(port.daily_pnl[:10]):
            print(f"  {ts.strftime('%Y-%m-%d')}: {format_currency(pnl)} ({format_percentage(pnl_pct)})")
        
        if len(port.daily_pnl) > 20:
            print("  ...")
            print("Last 10 Days:")
            for ts, pnl, pnl_pct in port.daily_pnl[-10:]:
                print(f"  {ts.strftime('%Y-%m-%d')}: {format_currency(pnl)} ({format_percentage(pnl_pct)})")
        
        # Calculate statistics
        pnl_values = [pnl for _, pnl, _ in port.daily_pnl]
        positive_days = sum(1 for pnl in pnl_values if pnl > 0)
        negative_days = sum(1 for pnl in pnl_values if pnl < 0)
        max_gain = max(pnl_values)
        max_loss = min(pnl_values)
        
        print(f"\nDaily P&L Statistics:")
        print(f"  Positive Days: {positive_days}")
        print(f"  Negative Days: {negative_days}")
        print(f"  Best Day: {format_currency(max_gain)}")
        print(f"  Worst Day: {format_currency(max_loss)}")
    
    # ===== FINAL RESULTS =====
    print("\n" + "=" * 60)
    print("🏁 FINAL RESULTS")
    print("=" * 60)
    
    initial_equity = equity_hist[0][1]
    final_equity = equity_hist[-1][1]
    total_return = final_equity - initial_equity
    percent_return = (total_return / initial_equity) * 100
    
    print(f"Initial Portfolio Value: {format_currency(initial_equity)}")
    print(f"Final Portfolio Value: {format_currency(final_equity)}")
    print(f"Total Return: {format_currency(total_return)} ({format_percentage(percent_return)})")
    print(f"Final Cash: {format_currency(port.cash)}")
    
    # Calculate max drawdown
    peak = initial_equity
    max_drawdown = 0
    for _, equity in equity_hist:
        if equity > peak:
            peak = equity
        drawdown = (peak - equity) / peak * 100
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    print(f"Maximum Drawdown: {max_drawdown:.2f}%")
    
    print("\n✅ Detailed backtest completed successfully!")

if __name__ == "__main__":
    main()
