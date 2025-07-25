# Statistical Arbitrage System with ML-Powered Signal Optimization

This project is a working prototype of a mean-reversion trading engine. It selects stock pairs that historically move together, waits for them to diverge, and then trades on the assumption that they'll snap back.

It's designed for real data, real logic, and is built like something you'd actually test in a quant setting.

---

## What It Does

- Picks stock pairs using cointegration (Engle-Granger method)
- Calculates spread and z-score to find trading signals
- Trains a machine learning model (XGBoost) to predict spread direction
- Backtests the strategy from 2015 to 2023
- Shows results with a live dashboard (Streamlit)

---

## Why I Built This

I wanted a project that reflects how actual quant trading systems work: modular, research-based, and measurable. I’m using this to explore stat arb research and also to show I can build something practical from scratch — data to prediction to signal.

---

## Features

- Cointegration-based pair selection (100+ S&P 500 stocks)
- Z-score strategy with entry and exit signals
- ML layer to predict spread direction (auto-labeling logic)
- Backtest engine with equity curve and daily P&L
- Streamlit dashboard with signals, spread, ML stats
- Git-tracked, modular codebase

---

## Folder Layout

stat-arb-engine/
│
├── data/               # OHLCV data from Yahoo Finance
├── engine/             # Signal logic, cointegration, ML
├── backtest/           # Strategy backtesting
├── dashboard/          # Streamlit UI
├── .gitignore
├── main.py             # Data download script
└── README.md

---

## How to Run

1. Install requirements  
   ```bash
   pip install -r requirements.txt

2. Download historical stock data
   python main.py

   	3.	Run cointegration test and generate trading signals
    python engine/cointegration.py
python engine/signal_generator.py

4.	Train the ML model to predict spread direction
python engine/spread_predictor.py

5.	Backtest the strategy using the signals
python backtest/backtester.py

6.	Launch the dashboard to visualize results
streamlit run dashboard/dashboard.py