"""
Train GradientBoostingRegressor for house price prediction.
Saves house_price_model.pkl and model_columns.pkl for the Flask app.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Paths relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAIN_CSV = os.path.join(BASE_DIR, "train.csv")
MODEL_PATH = os.path.join(BASE_DIR, "house_price_model.pkl")
COLUMNS_PATH = os.path.join(BASE_DIR, "model_columns.pkl")

# Features used in the web form (user-provided)
FORM_FEATURES = [
    "OverallQual",
    "GrLivArea",
    "GarageCars",
    "TotalBsmtSF",
    "FullBath",
    "YearBuilt",
]

# Additional numeric predictors for stronger model (missing at predict time -> 0)
EXTRA_NUMERIC = [
    "OverallCond",
    "YearRemodAdd",
    "1stFlrSF",
    "2ndFlrSF",
    "BsmtFullBath",
    "BsmtHalfBath",
    "HalfBath",
    "BedroomAbvGr",
    "TotRmsAbvGrd",
    "Fireplaces",
    "GarageArea",
    "WoodDeckSF",
    "OpenPorchSF",
    "MoSold",
    "YrSold",
]

MODEL_COLUMNS = FORM_FEATURES + EXTRA_NUMERIC


def load_and_prepare_data():
    """Load Ames housing train.csv and build feature matrix."""
    df = pd.read_csv(TRAIN_CSV)

    # Keep only columns that exist in the dataset
    cols = [c for c in MODEL_COLUMNS if c in df.columns]
    X = df[cols].copy()

    # Fill missing numeric values with median
    for col in X.columns:
        X[col] = pd.to_numeric(X[col], errors="coerce")
        X[col] = X[col].fillna(X[col].median())

    y = df["SalePrice"]
    return X, y, cols


def train_and_save():
    """Train model, evaluate, and persist artifacts."""
    X, y, feature_cols = load_and_prepare_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.08,
        max_depth=4,
        min_samples_split=5,
        min_samples_leaf=2,
        subsample=0.85,
        random_state=42,
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    print(f"Features: {len(feature_cols)}")
    print(f"Test MAE:  ${mae:,.0f}")
    print(f"Test R²:   {r2:.4f}")

    joblib.dump(model, MODEL_PATH)
    joblib.dump(feature_cols, COLUMNS_PATH)

    print(f"Saved model -> {MODEL_PATH}")
    print(f"Saved columns -> {COLUMNS_PATH}")


if __name__ == "__main__":
    train_and_save()
