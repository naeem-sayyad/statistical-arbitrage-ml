import os
import pandas as pd
import streamlit as st
import plotly.graph_objs as go

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIGNAL_FILE = os.path.join(BASE_DIR, "signals_KO_PEP_with_prediction.csv")
BACKTEST_FILE = os.path.join(BASE_DIR, "backtest_result_KO_PEP.csv")


st.set_page_config(layout="wide", page_title="Stat Arb Dashboard")

st.title(" Statistical Arbitrage Dashboard — KO vs PEP")

# Load Data
signal_df = pd.read_csv(SIGNAL_FILE, index_col="Date", parse_dates=True)
backtest_df = pd.read_csv(BACKTEST_FILE, index_col="Date", parse_dates=True)
# Spread & Z-Score Plot
st.subheader("Spread & Z-Score Signals")
fig1 = go.Figure()

fig1.add_trace(go.Scatter(x=signal_df.index, y=signal_df["spread"], name="Spread", line=dict(color='blue')))
fig1.add_trace(go.Scatter(x=signal_df.index, y=signal_df["zscore"], name="Z-Score", yaxis="y2", line=dict(color='orange')))

# Highlight signals
longs = signal_df[signal_df["long_signal"]]
shorts = signal_df[signal_df["short_signal"]]
exits = signal_df[signal_df["exit_signal"]]

fig1.add_trace(go.Scatter(x=longs.index, y=longs["spread"], mode="markers", name="Long", marker=dict(color="green", size=6)))
fig1.add_trace(go.Scatter(x=shorts.index, y=shorts["spread"], mode="markers", name="Short", marker=dict(color="red", size=6)))
fig1.add_trace(go.Scatter(x=exits.index, y=exits["spread"], mode="markers", name="Exit", marker=dict(color="gray", size=6)))
# ML Predicted Buy (upward spread) = 1
predicted_longs = signal_df[signal_df["predicted_direction"] == 1]
predicted_shorts = signal_df[signal_df["predicted_direction"] == 0]

fig1.add_trace(go.Scatter(
    x=predicted_longs.index, y=predicted_longs["spread"],
    mode="markers", name="Predicted Up", marker=dict(symbol="triangle-up", size=8, color="green", opacity=0.6)
))
fig1.add_trace(go.Scatter(
    x=predicted_shorts.index, y=predicted_shorts["spread"],
    mode="markers", name="Predicted Down", marker=dict(symbol="triangle-down", size=8, color="red", opacity=0.6)
))
fig1.update_layout(
    xaxis_title="Date",
    yaxis=dict(title="Spread"),
    yaxis2=dict(title="Z-Score", overlaying="y", side="right"),
    height=500,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig1, use_container_width=True)

# Equity Curve
st.subheader("💰 Equity Curve")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=backtest_df.index, y=backtest_df["equity"], name="Equity", line=dict(color="purple")))
fig2.update_layout(height=400, xaxis_title="Date", yaxis_title="Equity ($)")
st.plotly_chart(fig2, use_container_width=True)
# ML Prediction Summary
st.subheader("ML Prediction Summary")

col1, col2, col3 = st.columns(3)

total_up = (signal_df["predicted_direction"] == 1).sum()
total_down = (signal_df["predicted_direction"] == 0).sum()

# Optional: Calculate naive accuracy if spread direction matches
actual = signal_df["spread"].shift(-1) > signal_df["spread"]
pred = signal_df["predicted_direction"] == actual
accuracy = pred.mean() * 100

col1.metric("Predicted Up", total_up)
col2.metric("Predicted Down", total_down)
col3.metric("Approx Accuracy", f"{accuracy:.2f}%")

# Show recent predictions
st.markdown("#### Recent Predictions")
st.dataframe(signal_df[["spread", "zscore", "predicted_direction"]].tail(10))
st.caption("Statistical Arbitrage Engine | ML + Cointegration | Built by Naeem Sayyad")