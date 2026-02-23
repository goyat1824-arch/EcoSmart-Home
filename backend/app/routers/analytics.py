from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date, timedelta

from app.database import get_db
from app.services.co2_service import get_co2_data, get_total_co2
from app.services.cost_service import get_cost_data, get_total_cost
from app.services.sustainability_service import get_sustainability_score
from app.models.energy_reading import EnergyReading
from app.models.household import Household

router = APIRouter()


@router.get("/co2")
def co2_analytics(
    household_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    return get_co2_data(db, household_id, start_date, end_date)


@router.get("/cost")
def cost_analytics(
    household_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    return get_cost_data(db, household_id, start_date, end_date)


@router.get("/sustainability-score")
def sustainability_score(household_id: int, db: Session = Depends(get_db)):
    return get_sustainability_score(db, household_id)


@router.get("/summary")
def dashboard_summary(household_id: int, db: Session = Depends(get_db)):
    """Get complete dashboard summary for a household."""
    household = db.query(Household).filter(Household.id == household_id).first()
    if not household:
        return {"error": "Household not found"}

    # Get latest readings
    readings = (
        db.query(EnergyReading)
        .filter(EnergyReading.household_id == household_id)
        .order_by(EnergyReading.date.desc())
        .limit(365)
        .all()
    )

    if not readings:
        return {
            "today_kwh": 0, "yesterday_kwh": 0, "daily_change_pct": 0,
            "monthly_kwh": 0, "monthly_cost": 0, "monthly_co2_kg": 0,
            "sustainability_score": 50, "sustainability_grade": "C",
            "predicted_tomorrow_kwh": 0, "avg_daily_kwh_7d": 0,
        }

    today_kwh = readings[0].total_kwh if readings else 0
    yesterday_kwh = readings[1].total_kwh if len(readings) > 1 else 0
    daily_change = ((today_kwh - yesterday_kwh) / yesterday_kwh * 100) if yesterday_kwh > 0 else 0

    # Last 30 days
    last_30 = readings[:30]
    monthly_kwh = sum(r.total_kwh for r in last_30)
    monthly_cost = monthly_kwh * household.tariff_per_kwh
    monthly_co2 = monthly_kwh * household.emission_factor

    # 7-day average
    last_7 = readings[:7]
    avg_7d = sum(r.total_kwh for r in last_7) / len(last_7) if last_7 else 0

    # Sustainability score
    score_data = get_sustainability_score(db, household_id)

    # Prediction
    try:
        from app.ml.predictor import predict_daily
        preds = predict_daily(db, household_id, days=1)
        predicted = preds[0]["predicted_kwh"] if preds else 0
    except Exception:
        predicted = avg_7d  # Fallback to 7-day average

    return {
        "today_kwh": round(today_kwh, 2),
        "yesterday_kwh": round(yesterday_kwh, 2),
        "daily_change_pct": round(daily_change, 1),
        "monthly_kwh": round(monthly_kwh, 2),
        "monthly_cost": round(monthly_cost, 2),
        "monthly_co2_kg": round(monthly_co2, 2),
        "sustainability_score": score_data["score"],
        "sustainability_grade": score_data["grade"],
        "predicted_tomorrow_kwh": round(predicted, 2),
        "avg_daily_kwh_7d": round(avg_7d, 2),
    }


@router.get("/monthly-trend")
def monthly_trend(household_id: int, months: int = Query(default=12, le=48), db: Session = Depends(get_db)):
    """Get monthly aggregated energy data."""
    readings = (
        db.query(EnergyReading)
        .filter(EnergyReading.household_id == household_id)
        .order_by(EnergyReading.date)
        .all()
    )

    household = db.query(Household).filter(Household.id == household_id).first()
    if not readings or not household:
        return []

    # Group by month
    from collections import defaultdict
    monthly = defaultdict(lambda: {"kwh": 0, "count": 0})
    for r in readings:
        key = f"{r.date.year}-{r.date.month:02d}"
        monthly[key]["kwh"] += r.total_kwh
        monthly[key]["count"] += 1

    result = []
    for month_key in sorted(monthly.keys())[-months:]:
        data = monthly[month_key]
        kwh = data["kwh"]
        result.append({
            "month": month_key,
            "total_kwh": round(kwh, 2),
            "avg_daily_kwh": round(kwh / data["count"], 2),
            "cost": round(kwh * household.tariff_per_kwh, 2),
            "co2_kg": round(kwh * household.emission_factor, 2),
        })

    return result


@router.get("/appliance-breakdown")
def appliance_breakdown(
    household_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    """Get appliance category breakdown."""
    query = db.query(EnergyReading).filter(EnergyReading.household_id == household_id)
    if start_date:
        query = query.filter(EnergyReading.date >= start_date)
    if end_date:
        query = query.filter(EnergyReading.date <= end_date)

    readings = query.all()
    if not readings:
        return []

    kitchen = sum(r.sub_metering_kitchen for r in readings)
    laundry = sum(r.sub_metering_laundry for r in readings)
    hvac = sum(r.sub_metering_hvac for r in readings)
    total = sum(r.total_kwh for r in readings)
    other = max(0, total - kitchen - laundry - hvac)

    return [
        {"category": "Kitchen", "kwh": round(kitchen, 2), "percentage": round(kitchen / total * 100, 1) if total else 0},
        {"category": "Laundry", "kwh": round(laundry, 2), "percentage": round(laundry / total * 100, 1) if total else 0},
        {"category": "HVAC", "kwh": round(hvac, 2), "percentage": round(hvac / total * 100, 1) if total else 0},
        {"category": "Other", "kwh": round(other, 2), "percentage": round(other / total * 100, 1) if total else 0},
    ]
