import pandas as pd

def load_symbols(sym_to_path: dict):
    """
    Reads CSVs for one or more symbols.
    Each CSV must have columns: timestamp, open, high, low, close, volume.
    Returns:
      - data: dict {symbol: DataFrame}
      - timeline: list of sorted timestamps (union of all symbols)
    """
    data = {}
    for sym, path in sym_to_path.items():
        # Read CSV file
        df = pd.read_csv(path)
        # Convert timestamp to datetime
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        # Sort by timestamp and reset index
        df = df.sort_values("timestamp").reset_index(drop=True)
        # Select required columns
        data[sym] = df[["timestamp","open","high","low","close","volume"]]
    
    # Combine all timestamps into one sorted list
    all_ts = sorted(set().union(*[df["timestamp"].tolist() for df in data.values()]))
    return data, all_ts
