"""
Configuration file for the Elite Backtest Engine
"""

# Data Configuration
DATA_CONFIG = {
    "symbols": ["AAPL"],
    "data_paths": {
        "AAPL": "data/AAPL_2022.csv"
    },
    "date_range": {
        "start": "2022-01-01",
        "end": "2022-12-31"
    }
}

# Portfolio Configuration
PORTFOLIO_CONFIG = {
    "initial_cash": 100_000,
    "commission_rate": 0.001,  # 0.1% commission
    "min_trade_size": 100,     # Minimum trade size in dollars
}

# Execution Configuration
EXECUTION_CONFIG = {
    "slippage_bps": 5,         # 5 basis points slippage
    "fee_rate": 0.0001,        # 0.01% fee rate
    "fill_delay": 0,           # Bars to wait for fill (0 = immediate)
}

# Strategy Configuration
STRATEGY_CONFIG = {
    "buy_and_hold": {
        "cash_fraction": 0.95,
        "rebalance_frequency": "never"
    },
    "momentum": {
        "lookback_period": 20,
        "cash_fraction": 0.95,
        "stop_loss_pct": 0.10,
        "take_profit_pct": 0.20
    },
    "macross": {
        "fast_period": 5,
        "slow_period": 20,
        "cash_fraction": 0.95
    }
}

# Risk Management
RISK_CONFIG = {
    "max_position_size": 0.20,  # Max 20% in single position
    "max_drawdown": 0.25,       # Max 25% drawdown
    "position_sizing": "fixed",  # "fixed", "kelly", "volatility"
}

# Reporting Configuration
REPORTING_CONFIG = {
    "save_results": True,
    "output_dir": "results/",
    "plot_charts": True,
    "metrics": [
        "total_return",
        "sharpe_ratio", 
        "max_drawdown",
        "calmar_ratio",
        "win_rate"
    ]
}
