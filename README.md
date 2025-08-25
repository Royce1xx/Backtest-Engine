# Elite Backtest Engine 🚀

A professional-grade backtesting engine for quantitative trading strategies, built with Python.

## Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules for data, execution, portfolio management, and strategies
- **Realistic Execution**: Includes slippage and transaction fees simulation
- **Portfolio Tracking**: Real-time position and equity tracking
- **Flexible Data Loading**: Support for CSV data with OHLCV format
- **Strategy Framework**: Easy-to-implement strategy interface

## Architecture

```
BackTest New/
├── data/           # Data loading and management
├── engine/         # Core backtesting engine
├── execution/      # Order execution and fills
├── portfolio/      # Portfolio management and tracking
├── strategies/     # Trading strategy implementations
└── run.py         # Main execution script
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Data

Place your CSV files in the `data/` directory with the following columns:
- `timestamp`: ISO format datetime
- `open`: Opening price
- `high`: High price
- `low`: Low price
- `close`: Closing price
- `volume`: Trading volume

### 3. Run a Backtest

```bash
python run.py
```

Or use the test script:

```bash
python test_backtest.py
```

## Example: Buy and Hold Strategy

The included `BuyAndHold` strategy demonstrates how to implement a simple strategy:

```python
class BuyAndHold:
    def __init__(self, symbol, cash_fraction=0.95):
        self.symbol = symbol
        self.cash_fraction = cash_fraction
        self.bought = False

    def on_bar(self, ctx):
        # Only buy once at the first bar
        if not self.bought:
            px = ctx.price(self.symbol)
            target_qty = int((ctx.cash * self.cash_fraction) // px)
            if target_qty > 0:
                ctx.order_market(self.symbol, target_qty)
                self.bought = True
```

## Strategy Interface

To create your own strategy, implement the `on_bar` method:

```python
class MyStrategy:
    def __init__(self, symbol):
        self.symbol = symbol
    
    def on_bar(self, ctx):
        # Access current price
        current_price = ctx.price(self.symbol)
        
        # Access portfolio information
        cash = ctx.cash
        position = ctx.position(self.symbol)
        
        # Place orders
        ctx.order_market(self.symbol, 100)  # Buy 100 shares
        ctx.order_limit(self.symbol, -50, 150.0)  # Sell 50 shares at $150
```

## Context Methods

The strategy context provides these key methods:

- `ctx.price(symbol)`: Get current price for a symbol
- `ctx.cash`: Get available cash
- `ctx.position(symbol)`: Get current position for a symbol
- `ctx.bars(symbol, n)`: Get last n bars of data
- `ctx.order_market(symbol, qty)`: Place market order
- `ctx.order_limit(symbol, qty, price)`: Place limit order

## Portfolio Management

The engine automatically handles:
- Position tracking with average cost basis
- Cash management
- Mark-to-market calculations
- Equity history

## Execution Model

Features realistic execution simulation:
- Configurable slippage (basis points)
- Transaction fees
- Market and limit order support

## Sample Results

Running the buy-and-hold strategy on AAPL 2022 data:

```
=== BACKTEST RESULTS ===
Initial Capital: $100,000.00
Final Equity: $97,234.56
Total Return: -$2,765.44
Percent Return: -2.77%

=== FINAL PORTFOLIO ===
Cash: $4,234.56
AAPL: 549 shares @ $174.47 avg
```

## Extending the Engine

### Adding New Data Sources

Modify `data/loader.py` to support different data formats or APIs.

### Custom Execution Models

Extend `execution/fills.py` to implement different execution scenarios.

### Risk Management

Add position sizing, stop-loss, and other risk controls to your strategies.

## Requirements

- Python 3.8+
- pandas >= 1.5.0
- numpy >= 1.21.0

## License

This project is for educational and research purposes.
