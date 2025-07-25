import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def generate_zscore_signals(ticker1, ticker2, lookback=30, entry_z=2.0, exit_z=0.5):
    # Load prices
    df1 = pd.read_csv(os.path.join(DATA_DIR, f"{ticker1}.csv"), index_col="Date", parse_dates=True)
    df2 = pd.read_csv(os.path.join(DATA_DIR, f"{ticker2}.csv"), index_col="Date", parse_dates=True)

    df = pd.DataFrame()
    df[ticker1] = df1["Close"]
    df[ticker2] = df2["Close"]

    # Drop missing values
    df.dropna(inplace=True)

    # OLS hedge ratio
    hedge_ratio = np.polyfit(df[ticker2], df[ticker1], 1)[0]

    # Calculate spread
    df["spread"] = df[ticker1] - hedge_ratio * df[ticker2]

    # Rolling mean and std of spread
    df["zscore"] = (df["spread"] - df["spread"].rolling(lookback).mean()) / df["spread"].rolling(lookback).std()

    # Entry/exit signals
    df["long_signal"] = df["zscore"] <= -entry_z
    df["short_signal"] = df["zscore"] >= entry_z
    df["exit_signal"] = df["zscore"].abs() <= exit_z

    return df[["spread", "zscore", "long_signal", "short_signal", "exit_signal"]]

# Example usage
if __name__ == "__main__":
    ticker1 = "KO"
    ticker2 = "PEP"
    signal_df = generate_zscore_signals(ticker1, ticker2)
    signal_df.to_csv(os.path.join(BASE_DIR, f"signals_{ticker1}_{ticker2}.csv"))
    print(signal_df.tail(10))