import pandas as pd
import numpy as np


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create ML features from raw energy + weather data."""
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # Time-based features
    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["day_of_year"] = df["date"].dt.dayofyear
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

    # Season (Northern Hemisphere)
    df["season"] = df["month"].map({
        12: 0, 1: 0, 2: 0,   # Winter
        3: 1, 4: 1, 5: 1,    # Spring
        6: 2, 7: 2, 8: 2,    # Summer
        9: 3, 10: 3, 11: 3,  # Autumn
    })

    # Rolling averages
    df["rolling_7d_avg"] = df["total_kwh"].rolling(window=7, min_periods=1).mean()
    df["rolling_30d_avg"] = df["total_kwh"].rolling(window=30, min_periods=1).mean()
    df["rolling_7d_std"] = df["total_kwh"].rolling(window=7, min_periods=1).std().fillna(0)

    # Lag features
    df["lag_1d"] = df["total_kwh"].shift(1)
    df["lag_7d"] = df["total_kwh"].shift(7)
    df["lag_14d"] = df["total_kwh"].shift(14)

    # Temperature features (if available)
    if "avg_temp" in df.columns and df["avg_temp"].notna().any():
        df["temp_range"] = df["max_temp"] - df["min_temp"]
        df["temp_humidity_interaction"] = df["avg_temp"] * df["humidity"] / 100
        df["heating_degree_days"] = np.maximum(18 - df["avg_temp"], 0)
        df["cooling_degree_days"] = np.maximum(df["avg_temp"] - 24, 0)
    else:
        df["temp_range"] = 0
        df["temp_humidity_interaction"] = 0
        df["heating_degree_days"] = 0
        df["cooling_degree_days"] = 0

    # Sub-metering ratios
    total_sub = df["kitchen_kwh"] + df["laundry_kwh"] + df["hvac_kwh"]
    df["other_kwh"] = np.maximum(df["total_kwh"] - total_sub, 0)
    df["hvac_ratio"] = np.where(df["total_kwh"] > 0, df["hvac_kwh"] / df["total_kwh"], 0)

    # Fill NaN
    df = df.bfill().ffill().fillna(0)

    return df


def get_feature_columns() -> list[str]:
    """Return the list of feature columns used for training."""
    return [
        "day_of_week", "month", "day_of_year", "is_weekend", "season",
        "rolling_7d_avg", "rolling_30d_avg", "rolling_7d_std",
        "lag_1d", "lag_7d", "lag_14d",
        "avg_temp", "min_temp", "max_temp", "humidity", "wind_speed", "precipitation",
        "temp_range", "temp_humidity_interaction",
        "heating_degree_days", "cooling_degree_days",
        "kitchen_kwh", "laundry_kwh", "hvac_kwh",
        "hvac_ratio",
        "global_active_power", "voltage",
    ]
