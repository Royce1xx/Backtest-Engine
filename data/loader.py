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
        df = pd.read_csv(path)
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df = df.sort_values("timestamp").reset_index(drop=True)
        data[sym] = df[["timestamp","open","high","low","close","volume"]]
    # combine all timestamps into one sorted list
    all_ts = sorted(set().union(*[df["timestamp"].tolist() for df in data.values()]))
    return data, all_ts
