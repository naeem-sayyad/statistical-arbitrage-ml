import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIGNAL_FILE = os.path.join(BASE_DIR, "signals_KO_PEP.csv")

def backtest_pair_strategy(signal_df, capital=100000, position_size=10000):
    df = signal_df.copy()

    df["position"] = 0

    # Signal-based positions
    df.loc[df["long_signal"], "position"] = 1
    df.loc[df["short_signal"], "position"] = -1
    df.loc[df["exit_signal"], "position"] = 0

    # Forward fill position to maintain open trades
    df["position"] = df["position"].replace(to_replace=0, method="ffill").fillna(0)

    # Daily P&L = change in spread * position
    df["spread_change"] = df["spread"].diff()
    df["daily_pnl"] = df["spread_change"] * df["position"]

    # Cumulative returns
    df["cumulative_pnl"] = df["daily_pnl"].cumsum()
    df["equity"] = capital + df["cumulative_pnl"]

    return df

if __name__ == "__main__":
    signal_df = pd.read_csv(SIGNAL_FILE, index_col="Date", parse_dates=True)
    result = backtest_pair_strategy(signal_df)

    # Save results
    result.to_csv(os.path.join(BASE_DIR, "backtest_result_KO_PEP.csv"))

    print(result[["spread", "zscore", "position", "daily_pnl", "equity"]].tail(10))