from sqlalchemy.orm import Session
from datetime import date

from app.models.energy_reading import EnergyReading
from app.models.household import Household


def calculate_co2(energy_kwh: float, emission_factor: float) -> float:
    """Calculate CO2 emissions in kg from energy consumption."""
    return round(energy_kwh * emission_factor, 3)


def get_co2_data(
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
            "co2_kg": calculate_co2(r.total_kwh, household.emission_factor),
            "emission_factor": household.emission_factor,
        }
        for r in readings
    ]


def get_total_co2(db: Session, household_id: int, start_date: date | None = None, end_date: date | None = None) -> float:
    data = get_co2_data(db, household_id, start_date, end_date)
    return round(sum(d["co2_kg"] for d in data), 2)
