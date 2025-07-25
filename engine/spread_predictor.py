import os
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIGNAL_FILE = os.path.join(BASE_DIR, "signals_KO_PEP.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "signals_KO_PEP_with_prediction.csv")

def create_features(df, window=5):
    df = df.copy()

    # Lag features
    df["spread_lag1"] = df["spread"].shift(1)
    df["spread_lag2"] = df["spread"].shift(2)
    df["zscore_lag1"] = df["zscore"].shift(1)

    # Rolling features
    df["spread_rolling_mean"] = df["spread"].rolling(window).mean()
    df["spread_rolling_std"] = df["spread"].rolling(window).std()
    df["zscore_rolling_mean"] = df["zscore"].rolling(window).mean()

    # Target: 1 if spread goes up next day, else 0
    df["spread_next"] = df["spread"].shift(-1)
    df["target"] = (df["spread_next"] > df["spread"]).astype(int)

    df.dropna(inplace=True)
    return df

def train_xgb_classifier(df):
    features = [
        "spread_lag1", "spread_lag2", "zscore_lag1",
        "spread_rolling_mean", "spread_rolling_std", "zscore_rolling_mean"
    ]
    X = df[features]
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, shuffle=False, test_size=0.2
    )

    model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print(classification_report(y_test, preds))

    # Predict for entire dataset
    df["predicted_direction"] = model.predict(X)
    return df

if __name__ == "__main__":
    df = pd.read_csv(SIGNAL_FILE, index_col="Date", parse_dates=True)
    df_feat = create_features(df)
    df_predicted = train_xgb_classifier(df_feat)

    df_predicted.to_csv(OUTPUT_FILE)
    print(f"Saved: {OUTPUT_FILE}")
    print(df_predicted[["spread", "zscore", "predicted_direction"]].tail())