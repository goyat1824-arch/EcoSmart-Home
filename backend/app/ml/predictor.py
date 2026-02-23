import os
import numpy as np
import pandas as pd
import joblib
from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.models.energy_reading import EnergyReading
from app.models.weather import WeatherData
from app.ml.feature_engineering import engineer_features, get_feature_columns
from app.config import get_settings

settings = get_settings()

_model = None
_feature_columns = None


def _load_model():
    global _model, _feature_columns
    if _model is None:
        model_path = settings.MODEL_PATH
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}. Run training first.")
        _model = joblib.load(model_path)
        _feature_columns = joblib.load(settings.FEATURE_COLUMNS_PATH)
    return _model, _feature_columns


def predict_daily(db: Session, household_id: int, days: int = 7) -> list[dict]:
    """Predict energy consumption for the next N days."""
    model, feature_cols = _load_model()

    # Get recent readings for feature computation
    recent_readings = (
        db.query(EnergyReading)
        .filter(EnergyReading.household_id == household_id)
        .order_by(EnergyReading.date.desc())
        .limit(60)
        .all()
    )

    if not recent_readings:
        return []

    # Build a DataFrame from recent data
    energy_data = [{
        "date": r.date,
        "total_kwh": r.total_kwh,
        "peak_hour": r.peak_hour,
        "kitchen_kwh": r.sub_metering_kitchen,
        "laundry_kwh": r.sub_metering_laundry,
        "hvac_kwh": r.sub_metering_hvac,
        "global_active_power": r.global_active_power_avg,
        "voltage": r.voltage_avg,
    } for r in reversed(recent_readings)]

    df = pd.DataFrame(energy_data)

    # Get weather data
    last_date = recent_readings[0].date
    weather_records = db.query(WeatherData).order_by(WeatherData.date.desc()).limit(60).all()
    if weather_records:
        weather_df = pd.DataFrame([{
            "date": w.date,
            "avg_temp": w.avg_temp,
            "min_temp": w.min_temp,
            "max_temp": w.max_temp,
            "humidity": w.humidity,
            "wind_speed": w.wind_speed,
            "precipitation": w.precipitation,
        } for w in reversed(weather_records)])
        df = df.merge(weather_df, on="date", how="left")

    predictions = []
    for i in range(1, days + 1):
        pred_date = last_date + timedelta(days=i)

        # Extend df with a placeholder row for prediction
        new_row = df.iloc[-1].copy()
        new_row["date"] = pred_date
        # Use last known weather as approximation
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Re-engineer features
        featured_df = engineer_features(df)

        # Ensure all columns exist
        for col in feature_cols:
            if col not in featured_df.columns:
                featured_df[col] = 0

        X = featured_df[feature_cols].iloc[-1:].values
        pred_kwh = float(model.predict(X)[0])
        pred_kwh = max(0, pred_kwh)

        # Confidence interval (simple heuristic: +/- 15%)
        confidence_lower = pred_kwh * 0.85
        confidence_upper = pred_kwh * 1.15

        predictions.append({
            "date": pred_date.isoformat(),
            "predicted_kwh": round(pred_kwh, 2),
            "confidence_lower": round(confidence_lower, 2),
            "confidence_upper": round(confidence_upper, 2),
        })

        # Update the df with prediction for next iteration
        df.iloc[-1, df.columns.get_loc("total_kwh")] = pred_kwh

    return predictions


def predict_monthly(db: Session, household_id: int) -> dict:
    """Predict total energy for the current month."""
    daily_predictions = predict_daily(db, household_id, days=30)
    if not daily_predictions:
        return {"monthly_predicted_kwh": 0, "daily_predictions": []}

    total = sum(p["predicted_kwh"] for p in daily_predictions)
    return {
        "monthly_predicted_kwh": round(total, 2),
        "daily_predictions": daily_predictions,
    }


def get_model_metrics() -> dict | None:
    """Return training metrics if available."""
    metrics_path = "trained_models/training_results.joblib"
    if os.path.exists(metrics_path):
        results = joblib.load(metrics_path)
        return results
    return None
