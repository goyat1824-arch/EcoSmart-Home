from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta

from app.models.energy_reading import EnergyReading
from app.models.household import Household


# Baseline: average French household ~ 12.5 kWh/day
BASELINE_DAILY_KWH = 12.5


def get_sustainability_score(db: Session, household_id: int) -> dict:
    household = db.query(Household).filter(Household.id == household_id).first()
    if not household:
        return {"score": 0, "grade": "N/A"}

    # Get last 30 days of readings
    thirty_days_ago = date.today() - timedelta(days=30)
    recent_readings = (
        db.query(EnergyReading)
        .filter(EnergyReading.household_id == household_id)
        .order_by(EnergyReading.date.desc())
        .limit(30)
        .all()
    )

    if not recent_readings:
        return {
            "household_id": household_id,
            "score": 50.0,
            "grade": "C",
            "avg_daily_kwh": 0,
            "baseline_daily_kwh": BASELINE_DAILY_KWH,
            "trend": "stable",
            "co2_saved_kg": 0,
        }

    avg_daily = sum(r.total_kwh for r in recent_readings) / len(recent_readings)

    # Score: 100 if using 0, 0 if using 2x baseline
    ratio = avg_daily / BASELINE_DAILY_KWH
    score = max(0, min(100, (1 - (ratio - 0.5)) * 100))

    # Grade
    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    elif score >= 50:
        grade = "D"
    else:
        grade = "F"

    # Trend: compare first half vs second half of readings
    mid = len(recent_readings) // 2
    if mid > 0:
        first_half_avg = sum(r.total_kwh for r in recent_readings[mid:]) / (len(recent_readings) - mid)
        second_half_avg = sum(r.total_kwh for r in recent_readings[:mid]) / mid
        if second_half_avg < first_half_avg * 0.95:
            trend = "improving"
        elif second_half_avg > first_half_avg * 1.05:
            trend = "declining"
        else:
            trend = "stable"
    else:
        trend = "stable"

    # CO2 saved vs baseline
    total_kwh = sum(r.total_kwh for r in recent_readings)
    baseline_total = BASELINE_DAILY_KWH * len(recent_readings)
    co2_saved = max(0, (baseline_total - total_kwh) * household.emission_factor)

    return {
        "household_id": household_id,
        "score": round(score, 1),
        "grade": grade,
        "avg_daily_kwh": round(avg_daily, 2),
        "baseline_daily_kwh": BASELINE_DAILY_KWH,
        "trend": trend,
        "co2_saved_kg": round(co2_saved, 2),
    }
