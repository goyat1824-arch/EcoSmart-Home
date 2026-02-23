from sqlalchemy.orm import Session
from datetime import date

from app.models.energy_reading import EnergyReading
from app.models.household import Household


def calculate_cost(energy_kwh: float, tariff: float) -> float:
    """Calculate energy cost from consumption and tariff."""
    return round(energy_kwh * tariff, 2)


def get_cost_data(
    db: Session,
    household_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[dict]:
    household = db.query(Household).filter(Household.id == household_id).first()
    if not household:
        return []

    query = db.query(EnergyReading).filter(EnergyReading.household_id == household_id)
    if start_date:
        query = query.filter(EnergyReading.date >= start_date)
    if end_date:
        query = query.filter(EnergyReading.date <= end_date)

    readings = query.order_by(EnergyReading.date).all()
    return [
        {
            "date": r.date.isoformat(),
            "energy_kwh": round(r.total_kwh, 2),
            "cost": calculate_cost(r.total_kwh, household.tariff_per_kwh),
            "tariff": household.tariff_per_kwh,
        }
        for r in readings
    ]


def get_total_cost(db: Session, household_id: int, start_date: date | None = None, end_date: date | None = None) -> float:
    data = get_cost_data(db, household_id, start_date, end_date)
    return round(sum(d["cost"] for d in data), 2)
