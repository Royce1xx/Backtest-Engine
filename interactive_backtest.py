#!/usr/bin/env python3
"""
🚀 ELITE BACKTEST ENGINE - INTERACTIVE VERSION
Interactive backtesting with yfinance data and strategy selection
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from strategies.buy_and_hold import DynamicTrader
from strategies.macross import MACross
from strategies.simple_momentum import SimpleMomentum
from engine.engine import Engine
from portfolio.portfolio import Portfolio
from execution.fills import ExecutionModel

def get_user_input():
    """Get user input for backtest parameters"""
    print("🚀 ELITE BACKTEST ENGINE - INTERACTIVE SETUP")
    print("=" * 50)
    
    # Get symbol
    symbol = input("Enter stock symbol (e.g., AAPL, MSFT, TSLA): ").upper().strip()
    if not symbol:
        symbol = "AAPL"
        print(f"Using default symbol: {symbol}")
    
    # Get start date
    while True:
        start_input = input("Enter start date (YYYY-MM-DD) or year (YYYY): ").strip()
        try:
            if len(start_input) == 4:  # Just year
                start_date = datetime(int(start_input), 1, 1)
            else:  # Full date
                start_date = datetime.strptime(start_input, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD or YYYY")
    
    # Get end date
    while True:
        end_input = input("Enter end date (YYYY-MM-DD) or 'now' for current date: ").strip()
        try:
            if end_input.lower() == 'now':
                end_date = datetime.now()
            elif len(end_input) == 4:  # Just year
                end_date = datetime(int(end_input), 12, 31)
            else:  # Full date
                end_date = datetime.strptime(end_input, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD, YYYY, or 'now'")
    
    # Get initial capital
    while True:
        try:
            capital = float(input("Enter initial capital (default: $100,000): ") or "100000")
            if capital > 0:
                break
            else:
                print("Capital must be positive")
        except ValueError:
            print("Invalid number")
    
    # Get strategy choice
    print("\nAvailable Strategies:")
    print("1. Buy & Hold (Dynamic)")
    print("2. Moving Average Crossover (MACross)")
    print("3. Simple Momentum")
    
    while True:
        try:
            strategy_choice = int(input("Choose strategy (1-3): "))
            if strategy_choice in [1, 2, 3]:
                break
            else:
                print("Please choose 1, 2, or 3")
        except ValueError:
            print("Please enter a number")
    
    return symbol, start_date, end_date, capital, strategy_choice

def download_data(symbol, start_date, end_date):
    """Download data from yfinance"""
    print(f"\n📥 Downloading {symbol} data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")
    
    try:
        # Download data
        ticker = yf.Ticker(symbol)
        data = ticker.history(start=start_date, end=end_date)
        
        if data.empty:
            print(f"❌ No data found for {symbol} in the specified date range")
            return None
        
        # Clean and format data - yfinance has different column names
        data = data.reset_index()
        
        # Map yfinance columns to our expected format
        column_mapping = {
            'Date': 'timestamp',
            'Open': 'open',
            'High': 'high', 
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        }
        
        # Rename columns
        data = data.rename(columns=column_mapping)
        
        # Ensure we have the required columns
        required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        if not all(col in data.columns for col in required_columns):
            print(f"❌ Missing required columns. Available: {list(data.columns)}")
            return None
        
        # Select only the required columns in the right order
        data = data[required_columns]
        
        # Convert timestamp to datetime
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        
        print(f"✅ Downloaded {len(data)} data points")
        print(f"📊 Date range: {data['timestamp'].min().strftime('%Y-%m-%d')} to {data['timestamp'].max().strftime('%Y-%m-%d')}")
        print(f"💰 Price range: ${data['low'].min():.2f} - ${data['high'].max():.2f}")
        
        return data
        
    except Exception as e:
        print(f"❌ Error downloading data: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_strategy(strategy_choice, symbol, capital):
    """Create strategy instance based on user choice"""
    if strategy_choice == 1:
        print("🎯 Using Dynamic Trader Strategy")
        return DynamicTrader(symbol=symbol, cash_fraction=0.95, profit_target=0.15, stop_loss=0.08)
    elif strategy_choice == 2:
        print("📈 Using Moving Average Crossover Strategy")
        return MACross(symbol=symbol, short_window=10, long_window=30)
    elif strategy_choice == 3:
        print("⚡ Using Simple Momentum Strategy")
        return SimpleMomentum(symbol=symbol, lookback=20, threshold=0.02)
    else:
        raise ValueError("Invalid strategy choice")

def run_backtest(data, strategy, initial_capital):
    """Run the backtest"""
    print(f"\n🚀 Starting backtest with ${initial_capital:,.2f} initial capital...")
    
    # Create engine components
    portfolio = Portfolio(initial_capital)
    execution_model = ExecutionModel()
    
    # Create data dict with symbol as key
    data_dict = {data.columns[0]: data}  # Use first column name as key
    
    # Create engine and run
    engine = Engine(data, data["timestamp"].tolist(), portfolio, execution_model)
    engine.run(strategy)
    
    return portfolio

def display_results(portfolio, symbol, start_date, end_date):
    """Display comprehensive backtest results"""
    print("\n" + "="*60)
    print("📊 BACKTEST RESULTS")
    print("="*60)
    
    # Basic metrics
    initial_equity = portfolio.equity_history[0][1] if portfolio.equity_history else 0
    final_equity = portfolio.equity_history[-1][1] if portfolio.equity_history else 0
    total_return = final_equity - initial_equity
    total_return_pct = (total_return / initial_equity * 100) if initial_equity > 0 else 0
    
    print(f"📅 Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"💰 Initial Capital: ${initial_equity:,.2f}")
    print(f"💰 Final Equity: ${final_equity:,.2f}")
    print(f"📈 Total Return: ${total_return:,.2f} ({total_return_pct:+.2f}%)")
    print(f"💵 Current Cash: ${portfolio.cash:,.2f}")
    
    # Position summary
    if portfolio.positions:
        print(f"\n📋 Current Positions:")
        for symbol, pos in portfolio.positions.items():
            if pos["qty"] != 0:
                current_value = pos["qty"] * pos["avg"]
                print(f"   {symbol}: {pos['qty']} shares @ ${pos['avg']:.2f} = ${current_value:,.2f}")
    
    # Trade summary
    if portfolio.trade_history:
        print(f"\n🔄 Trading Summary:")
        print(f"   Total Trades: {len(portfolio.trade_history)}")
        
        buy_trades = [t for t in portfolio.trade_history if t["type"] == "BUY"]
        sell_trades = [t for t in portfolio.trade_history if t["type"] == "SELL"]
        
        if buy_trades:
            total_bought = sum(t["total_value"] for t in buy_trades)
            print(f"   Total Bought: ${total_bought:,.2f}")
        
        if sell_trades:
            total_sold = sum(t["total_value"] for t in sell_trades)
            print(f"   Total Sold: ${total_sold:,.2f}")
    
    # Daily P&L summary
    if portfolio.daily_pnl:
        daily_returns = [pnl[2] for pnl in portfolio.daily_pnl if pnl[2] != 0]
        if daily_returns:
            avg_daily_return = sum(daily_returns) / len(daily_returns)
            best_day = max(daily_returns)
            worst_day = min(daily_returns)
            print(f"\n📊 Daily Performance:")
            print(f"   Average Daily Return: {avg_daily_return:+.2f}%")
            print(f"   Best Day: {best_day:+.2f}%")
            print(f"   Worst Day: {worst_day:+.2f}%")

def main():
    """Main function"""
    try:
        # Get user input
        symbol, start_date, end_date, capital, strategy_choice = get_user_input()
        
        # Download data
        data = download_data(symbol, start_date, end_date)
        if data is None:
            return
        
        # Create strategy
        strategy = create_strategy(strategy_choice, symbol, capital)
        
        # Run backtest
        portfolio = run_backtest(data, strategy, capital)
        
        # Display results
        display_results(portfolio, symbol, start_date, end_date)
        
        print(f"\n🎉 Backtest completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n❌ Backtest cancelled by user")
    except Exception as e:
        print(f"\n❌ Error during backtest: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
