import os
import pandas as pd
from statsmodels.tsa.stattools import coint
from itertools import combinations

# Define data directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Load all close prices into one DataFrame
def load_close_prices():
    all_data = {}
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".csv"):
            ticker = filename.replace(".csv", "")
            file_path = os.path.join(DATA_DIR, filename)

            try:
                df = pd.read_csv(file_path, index_col="Date", parse_dates=True)
                if 'Close' in df.columns:
                    all_data[ticker] = df['Close']
                else:
                    print(f"Skipping {ticker}: 'Close' column missing")
            except Exception as e:
                print(f"Skipping {ticker}: {e}")
    return pd.DataFrame(all_data).dropna(axis=0)
# Run Engle-Granger test on all pairs
def find_cointegrated_pairs(data, significance_level=0.05):
    pairs = list(combinations(data.columns, 2))
    cointegrated_pairs = []

    for stock1, stock2 in pairs:
        series1 = data[stock1]
        series2 = data[stock2]

        score, pvalue, _ = coint(series1, series2)

        if pvalue < significance_level:
            cointegrated_pairs.append((stock1, stock2, pvalue))

    return sorted(cointegrated_pairs, key=lambda x: x[2])

# Main execution
if __name__ == "__main__":
    print("Loading price data...")
    price_df = load_close_prices()

    print("Finding cointegrated pairs...")
    cointegrated = find_cointegrated_pairs(price_df)

    result_df = pd.DataFrame(cointegrated, columns=["Stock 1", "Stock 2", "p-value"])
    result_df.to_csv(os.path.join(BASE_DIR, "cointegrated_pairs.csv"), index=False)
    print(result_df)