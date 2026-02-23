"""
EcoSmart Home - Data Seeding Script

Downloads UCI Household Electric Power Consumption dataset and weather data,
processes it, and seeds the database.

Usage:
    cd backend
    python seed_data.py
"""
import os
import sys
import zipfile
import io
from datetime import date

import httpx
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal, create_tables, Base
from app.models.user import User
from app.models.household import Household
from app.models.appliance import Appliance
from app.models.energy_reading import EnergyReading
from app.models.weather import WeatherData


# --- Configuration ---
UCI_DATASET_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip"
DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "household_power_consumption.txt")

# Sceaux, France coordinates
LATITUDE = 48.78
LONGITUDE = 2.29


def download_dataset():
    """Download and extract the UCI dataset."""
    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(CSV_PATH):
        print(f"  Dataset already exists at {CSV_PATH}")
        return

    print(f"  Downloading UCI Household Power Consumption dataset...")
    print(f"  URL: {UCI_DATASET_URL}")

    response = httpx.get(UCI_DATASET_URL, follow_redirects=True, timeout=120)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        zf.extractall(DATA_DIR)

    print(f"  Downloaded and extracted to {DATA_DIR}/")


def load_and_process_energy_data() -> pd.DataFrame:
    """Load UCI dataset and aggregate to daily summaries."""
    print("  Reading CSV (this may take a moment for 2M+ rows)...")
    df = pd.read_csv(
        CSV_PATH,
        sep=";",
        low_memory=False,
        na_values=["?"],
    )

    print(f"  Raw records: {len(df):,}")

    # Parse datetime
    df["datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], format="%d/%m/%Y %H:%M:%S")
    df["date"] = df["datetime"].dt.date
    df["hour"] = df["datetime"].dt.hour

    # Convert to numeric
    numeric_cols = ["Global_active_power", "Global_reactive_power", "Voltage",
                    "Global_intensity", "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows with missing power data
    df = df.dropna(subset=["Global_active_power"])
    print(f"  Valid records: {len(df):,}")

    # Aggregate to daily
    # Global_active_power is in kW (minute average), convert to kWh per day
    # Each record = 1 minute, so kWh = kW * (1/60)
    daily = df.groupby("date").agg(
        total_kwh=("Global_active_power", lambda x: x.sum() / 60),  # kW-minutes -> kWh
        global_active_power_avg=("Global_active_power", "mean"),
        voltage_avg=("Voltage", "mean"),
        sub_metering_1=("Sub_metering_1", lambda x: x.sum() / 1000),  # Wh -> kWh
        sub_metering_2=("Sub_metering_2", lambda x: x.sum() / 1000),
        sub_metering_3=("Sub_metering_3", lambda x: x.sum() / 1000),
        record_count=("Global_active_power", "count"),
    ).reset_index()

    # Find peak hour per day
    peak_hours = df.groupby("date").apply(
        lambda x: x.groupby("hour")["Global_active_power"].sum().idxmax()
    ).reset_index()
    peak_hours.columns = ["date", "peak_hour"]
    daily = daily.merge(peak_hours, on="date")

    # Filter days with sufficient data (at least 1000 minutes = ~17 hours)
    daily = daily[daily["record_count"] >= 1000]
    daily = daily.drop(columns=["record_count"])

    print(f"  Daily records: {len(daily)}")
    print(f"  Date range: {daily['date'].min()} to {daily['date'].max()}")
    print(f"  Avg daily consumption: {daily['total_kwh'].mean():.2f} kWh")

    return daily


def fetch_weather_data(start_year: int, end_year: int) -> pd.DataFrame:
    """Fetch historical weather data from Open-Meteo API."""
    print(f"  Fetching weather data for Sceaux, France ({start_year}-{end_year})...")

    all_weather = []
    for year in range(start_year, end_year + 1):
        url = (
            f"https://archive-api.open-meteo.com/v1/archive"
            f"?latitude={LATITUDE}&longitude={LONGITUDE}"
            f"&start_date={year}-01-01&end_date={year}-12-31"
            f"&daily=temperature_2m_mean,temperature_2m_min,temperature_2m_max,"
            f"relative_humidity_2m_mean,wind_speed_10m_max,precipitation_sum"
            f"&timezone=Europe/Paris"
        )
        try:
            response = httpx.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            daily = data.get("daily", {})
            if daily and daily.get("time"):
                for i, d in enumerate(daily["time"]):
                    all_weather.append({
                        "date": d,
                        "avg_temp": daily.get("temperature_2m_mean", [None])[i],
                        "min_temp": daily.get("temperature_2m_min", [None])[i],
                        "max_temp": daily.get("temperature_2m_max", [None])[i],
                        "humidity": daily.get("relative_humidity_2m_mean", [None])[i],
                        "wind_speed": daily.get("wind_speed_10m_max", [None])[i],
                        "precipitation": daily.get("precipitation_sum", [0])[i] or 0,
                    })
                print(f"    {year}: {len(daily['time'])} days")
        except Exception as e:
            print(f"    {year}: Failed ({e})")

    if all_weather:
        weather_df = pd.DataFrame(all_weather)
        weather_df["date"] = pd.to_datetime(weather_df["date"]).dt.date
        return weather_df
    return pd.DataFrame()


def seed_database():
    print("\n" + "=" * 60)
    print("  EcoSmart Home - Data Seeding")
    print("=" * 60)

    # Create tables
    print("\n[1/6] Creating database tables...")
    create_tables()
    print("  Done.")

    # Download dataset
    print("\n[2/6] Downloading dataset...")
    download_dataset()

    # Process energy data
    print("\n[3/6] Processing energy data...")
    daily_energy = load_and_process_energy_data()

    # Fetch weather
    print("\n[4/6] Fetching weather data...")
    date_min = daily_energy["date"].min()
    date_max = daily_energy["date"].max()
    weather_df = fetch_weather_data(date_min.year, date_max.year)
    print(f"  Weather records: {len(weather_df)}")

    # Seed to database
    print("\n[5/6] Seeding database...")
    db = SessionLocal()
    try:
        # Check if already seeded
        existing_count = db.query(EnergyReading).count()
        if existing_count > 0:
            print(f"  Database already has {existing_count} readings. Clearing...")
            db.query(EnergyReading).delete()
            db.query(WeatherData).delete()
            db.query(Appliance).delete()
            db.query(Household).delete()
            db.query(User).delete()
            db.commit()

        # Create user
        user = User(name="Demo User", email="demo@ecosmart.com", country="France")
        db.add(user)
        db.flush()

        # Create household
        household = Household(
            user_id=user.id,
            name="Demo Household - Sceaux",
            address="7 Rue de Sceaux",
            city="Sceaux",
            latitude=LATITUDE,
            longitude=LONGITUDE,
            tariff_per_kwh=0.174,
            emission_factor=0.055,
        )
        db.add(household)
        db.flush()

        # Create appliances (mapped to UCI sub-metering categories)
        appliances = [
            Appliance(household_id=household.id, name="Dishwasher", category="Kitchen", watt_rating=1800, avg_usage_hours=1.5, efficiency_rating=3),
            Appliance(household_id=household.id, name="Oven", category="Kitchen", watt_rating=2500, avg_usage_hours=1.0, efficiency_rating=3),
            Appliance(household_id=household.id, name="Microwave", category="Kitchen", watt_rating=1200, avg_usage_hours=0.5, efficiency_rating=4),
            Appliance(household_id=household.id, name="Washing Machine", category="Laundry", watt_rating=2200, avg_usage_hours=1.0, efficiency_rating=3),
            Appliance(household_id=household.id, name="Dryer", category="Laundry", watt_rating=3000, avg_usage_hours=0.8, efficiency_rating=2),
            Appliance(household_id=household.id, name="Refrigerator", category="Laundry", watt_rating=150, avg_usage_hours=24.0, efficiency_rating=4),
            Appliance(household_id=household.id, name="Water Heater", category="HVAC", watt_rating=4500, avg_usage_hours=3.0, efficiency_rating=3),
            Appliance(household_id=household.id, name="Air Conditioner", category="HVAC", watt_rating=3500, avg_usage_hours=4.0, efficiency_rating=2),
            Appliance(household_id=household.id, name="Lighting", category="Lighting", watt_rating=500, avg_usage_hours=6.0, efficiency_rating=4),
        ]
        db.add_all(appliances)

        # Insert energy readings
        print("  Inserting energy readings...")
        readings = []
        for _, row in daily_energy.iterrows():
            readings.append(EnergyReading(
                household_id=household.id,
                date=row["date"],
                total_kwh=round(row["total_kwh"], 3),
                peak_hour=int(row["peak_hour"]),
                sub_metering_kitchen=round(row["sub_metering_1"], 3),
                sub_metering_laundry=round(row["sub_metering_2"], 3),
                sub_metering_hvac=round(row["sub_metering_3"], 3),
                global_active_power_avg=round(row["global_active_power_avg"], 4),
                voltage_avg=round(row["voltage_avg"], 2),
            ))

        db.bulk_save_objects(readings)
        print(f"  Inserted {len(readings)} energy readings")

        # Insert weather data
        if not weather_df.empty:
            print("  Inserting weather data...")
            weather_records = []
            for _, row in weather_df.iterrows():
                weather_records.append(WeatherData(
                    date=row["date"],
                    city="Sceaux",
                    avg_temp=row["avg_temp"],
                    min_temp=row["min_temp"],
                    max_temp=row["max_temp"],
                    humidity=row["humidity"],
                    wind_speed=row["wind_speed"],
                    precipitation=row["precipitation"],
                ))
            db.bulk_save_objects(weather_records)
            print(f"  Inserted {len(weather_records)} weather records")

        db.commit()
        print("\n[6/6] Verification...")
        print(f"  Users: {db.query(User).count()}")
        print(f"  Households: {db.query(Household).count()}")
        print(f"  Appliances: {db.query(Appliance).count()}")
        print(f"  Energy Readings: {db.query(EnergyReading).count()}")
        print(f"  Weather Records: {db.query(WeatherData).count()}")
        print("\nSeeding complete!")

    except Exception as e:
        db.rollback()
        print(f"\nERROR: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
