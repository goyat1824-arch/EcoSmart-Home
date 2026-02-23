import pandas as pd
from sqlalchemy.orm import Session

from app.models.energy_reading import EnergyReading
from app.models.weather import WeatherData


def load_training_data(db: Session, household_id: int) -> pd.DataFrame:
    """Load and merge energy + weather data for ML training."""
    # Fetch energy readings
    readings = db.query(EnergyReading).filter(
        EnergyReading.household_id == household_id
    ).order_by(EnergyReading.date).all()

    if not readings:
        return pd.DataFrame()

    energy_df = pd.DataFrame([{
        "date": r.date,
        "total_kwh": r.total_kwh,
        "peak_hour": r.peak_hour,
        "kitchen_kwh": r.sub_metering_kitchen,
        "laundry_kwh": r.sub_metering_laundry,
        "hvac_kwh": r.sub_metering_hvac,
        "global_active_power": r.global_active_power_avg,
        "voltage": r.voltage_avg,
    } for r in readings])

    # Fetch weather data
    weather = db.query(WeatherData).order_by(WeatherData.date).all()
    if weather:
        weather_df = pd.DataFrame([{
            "date": w.date,
            "avg_temp": w.avg_temp,
            "min_temp": w.min_temp,
            "max_temp": w.max_temp,
            "humidity": w.humidity,
            "wind_speed": w.wind_speed,
            "precipitation": w.precipitation,
        } for w in weather])

        # Merge on date
        df = energy_df.merge(weather_df, on="date", how="left")
    else:
        df = energy_df
        df["avg_temp"] = None
        df["min_temp"] = None
        df["max_temp"] = None
        df["humidity"] = None
        df["wind_speed"] = None
        df["precipitation"] = None

    return df
