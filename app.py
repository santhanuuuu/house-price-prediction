"""
House Price Prediction — Flask Web Application
Loads a trained scikit-learn model and serves predictions via a REST-style form API.
"""

import os
import traceback
import joblib  # pyright: ignore[reportMissingImports]
import pandas as pd  # pyright: ignore[reportMissingImports]
import numpy as np  # pyright: ignore[reportMissingImports]
from flask import Flask, render_template, request, jsonify  # pyright: ignore[reportMissingImports]

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "house_price_model.pkl")
COLUMNS_PATH = os.path.join(BASE_DIR, "model_columns.pkl")

# Form fields exposed in the UI
FORM_FIELDS = [
    "OverallQual",
    "GrLivArea",
    "GarageCars",
    "TotalBsmtSF",
    "FullBath",
    "YearBuilt",
]

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Global model artifacts (loaded once at startup)
model = None
model_columns = None


def load_artifacts():
    """Load trained model and column list from disk."""
    global model, model_columns

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Run: python train_model.py"
        )
    if not os.path.exists(COLUMNS_PATH):
        raise FileNotFoundError(
            f"Column list not found at {COLUMNS_PATH}. Run: python train_model.py"
        )

    model = joblib.load(MODEL_PATH)
    model_columns = joblib.load(COLUMNS_PATH)


def build_input_dataframe(form_data):
    """
    Convert form inputs into a single-row DataFrame aligned with training columns.
    Missing columns are filled with 0; column order matches model_columns.
    """
    row = {}
    for field in FORM_FIELDS:
        raw = form_data.get(field, "")
        if raw is None or str(raw).strip() == "":
            raise ValueError(f"Missing required field: {field}")
        try:
            row[field] = float(raw)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid number for {field}: {raw}")

    input_df = pd.DataFrame([row])

    # Align with training feature set
    for col in model_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[model_columns]
    return input_df


def format_price(value):
    """Format prediction as USD currency string."""
    return f"${value:,.0f}"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    """Render the prediction dashboard."""
    return render_template("index.html", fields=FORM_FIELDS)


@app.route("/predict", methods=["POST"])
def predict():
    """
    Accept JSON or form-encoded inputs, run model inference, return prediction.
    """
    try:
        if model is None or model_columns is None:
            load_artifacts()

        # Support both JSON (fetch) and standard form posts
        if request.is_json:
            payload = request.get_json(silent=True) or {}
        else:
            payload = request.form.to_dict()

        input_df = build_input_dataframe(payload)
        prediction = float(model.predict(input_df)[0])
        prediction = max(prediction, 0)  # Prices cannot be negative

        return jsonify(
            {
                "success": True,
                "predicted_price": prediction,
                "formatted_price": format_price(prediction),
                "inputs": {k: payload.get(k) for k in FORM_FIELDS},
            }
        )

    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400

    except FileNotFoundError as exc:
        return jsonify({"success": False, "error": str(exc)}), 503

    except Exception as exc:
        app.logger.error("Prediction error: %s\n%s", exc, traceback.format_exc())
        return jsonify(
            {"success": False, "error": "An unexpected error occurred during prediction."}
        ), 500


@app.errorhandler(404)
def not_found(error):
    """Handle unknown routes."""
    if request.path.startswith("/predict") or request.accept_mimetypes.accept_json:
        return jsonify({"success": False, "error": "Endpoint not found."}), 404
    return render_template("index.html", fields=FORM_FIELDS), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle server errors."""
    return jsonify({"success": False, "error": "Internal server error."}), 500


# ---------------------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        load_artifacts()
        print("Model and columns loaded successfully.")
        print(f"Feature count: {len(model_columns)}")
    except FileNotFoundError as e:
        print(f"WARNING: {e}")

    # debug=True for development; set debug=False in production
    app.run(host="0.0.0.0", port=5000, debug=True)
