from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models.energy_reading import EnergyReading
from app.models.household import Household
from app.schemas.energy import EnergyReadingCreate, EnergyReadingResponse

router = APIRouter()


@router.post("/", response_model=EnergyReadingResponse, status_code=201)
def create_reading(reading: EnergyReadingCreate, db: Session = Depends(get_db)):
    household = db.query(Household).filter(Household.id == reading.household_id).first()
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")
    db_reading = EnergyReading(**reading.model_dump())
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading


@router.get("/", response_model=list[EnergyReadingResponse])
def list_readings(
    household_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = Query(default=365, le=1500),
    db: Session = Depends(get_db),
):
    query = db.query(EnergyReading).filter(EnergyReading.household_id == household_id)
    if start_date:
        query = query.filter(EnergyReading.date >= start_date)
    if end_date:
        query = query.filter(EnergyReading.date <= end_date)
    return query.order_by(EnergyReading.date.desc()).limit(limit).all()


@router.get("/daily-summary")
def daily_summary(
    household_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(EnergyReading).filter(EnergyReading.household_id == household_id)
    if start_date:
        query = query.filter(EnergyReading.date >= start_date)
    if end_date:
        query = query.filter(EnergyReading.date <= end_date)

    readings = query.order_by(EnergyReading.date).all()
    return [
        {
            "date": r.date.isoformat(),
            "total_kwh": round(r.total_kwh, 2),
            "kitchen_kwh": round(r.sub_metering_kitchen, 2),
            "laundry_kwh": round(r.sub_metering_laundry, 2),
            "hvac_kwh": round(r.sub_metering_hvac, 2),
            "peak_hour": r.peak_hour,
        }
        for r in readings
    ]
