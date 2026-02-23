"""
ML Training Pipeline for EcoSmart Home.

Usage:
    cd backend
    python -m app.ml.train
"""
import sys
import os
import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SessionLocal
from app.ml.data_loader import load_training_data
from app.ml.feature_engineering import engineer_features, get_feature_columns


def evaluate_model(name: str, y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    print(f"\n{'='*40}")
    print(f"  {name}")
    print(f"{'='*40}")
    print(f"  MAE:  {mae:.4f} kWh")
    print(f"  RMSE: {rmse:.4f} kWh")
    print(f"  R2:   {r2:.4f}")
    return {"name": name, "mae": mae, "rmse": rmse, "r2": r2}


def train_models():
    print("\n" + "=" * 60)
    print("  EcoSmart Home - ML Training Pipeline")
    print("=" * 60)

    db = SessionLocal()
    try:
        # Load data
        print("\n[1/5] Loading data from database...")
        df = load_training_data(db, household_id=1)
        if df.empty:
            print("ERROR: No data found. Run seed_data.py first.")
            return
        print(f"  Loaded {len(df)} daily records")

        # Feature engineering
        print("\n[2/5] Engineering features...")
        df = engineer_features(df)
        feature_cols = get_feature_columns()

        # Ensure all feature columns exist
        for col in feature_cols:
            if col not in df.columns:
                df[col] = 0

        X = df[feature_cols].values
        y = df["total_kwh"].values
        print(f"  Features: {len(feature_cols)}")
        print(f"  Samples: {len(X)}")

        # Chronological split (80/20)
        print("\n[3/5] Splitting data (80/20 chronological)...")
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        print(f"  Train: {len(X_train)} | Test: {len(X_test)}")

        # Train models
        print("\n[4/5] Training models...")
        models = {
            "Linear Regression": LinearRegression(),
            "Random Forest": RandomForestRegressor(
                n_estimators=200, max_depth=15, min_samples_split=5, random_state=42, n_jobs=-1
            ),
            "XGBoost": XGBRegressor(
                n_estimators=300, max_depth=8, learning_rate=0.05,
                subsample=0.8, colsample_bytree=0.8, random_state=42,
            ),
        }

        results = []
        trained_models = {}
        for name, model in models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            result = evaluate_model(name, y_test, y_pred)
            results.append(result)
            trained_models[name] = model

        # Select best model by R2
        best = max(results, key=lambda x: x["r2"])
        print(f"\n{'='*60}")
        print(f"  BEST MODEL: {best['name']}")
        print(f"  R2 = {best['r2']:.4f} | MAE = {best['mae']:.4f} kWh")
        print(f"{'='*60}")

        # Save best model
        print("\n[5/5] Saving best model...")
        os.makedirs("trained_models", exist_ok=True)
        joblib.dump(trained_models[best["name"]], "trained_models/best_model.joblib")
        joblib.dump(feature_cols, "trained_models/feature_columns.joblib")
        joblib.dump(results, "trained_models/training_results.joblib")
        print("  Saved to trained_models/best_model.joblib")

        # Feature importance (if tree-based)
        best_model = trained_models[best["name"]]
        if hasattr(best_model, "feature_importances_"):
            importances = best_model.feature_importances_
            feature_imp = sorted(zip(feature_cols, importances), key=lambda x: x[1], reverse=True)
            print("\n  Top 10 Features:")
            for feat, imp in feature_imp[:10]:
                print(f"    {feat:30s} {imp:.4f}")

        print("\nTraining complete!")
    finally:
        db.close()


if __name__ == "__main__":
    train_models()
