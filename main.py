import os
import yfinance as yf
import pandas as pd

# Define storage folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Sample list of S&P 500 tickers (replace with full list later)
sp500_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "JPM", "JNJ", "XOM", "V", "NVDA", "KO", "PEP"]

# Define date range
start_date = "2015-01-01"
end_date = "2023-12-31"

# Download and save each ticker's data
for ticker in sp500_tickers:
    print(f"Downloading {ticker}...")
    try:
        df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False, progress=False)
        
        # Flatten column index if multi-indexed (common in new yfinance versions)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        if not df.empty:
            df.to_csv(os.path.join(DATA_DIR, f"{ticker}.csv"), index_label="Date")
            print(f"Saved {ticker}.csv")
        else:
            print(f"No data for {ticker}")
    except Exception as e:
        print(f"Error downloading {ticker}: {e}")