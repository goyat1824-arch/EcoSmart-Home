from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.appliance import Appliance
from app.models.household import Household
from app.schemas.appliance import ApplianceCreate, ApplianceUpdate, ApplianceResponse

router = APIRouter()


@router.post("/", response_model=ApplianceResponse, status_code=201)
def create_appliance(appliance: ApplianceCreate, db: Session = Depends(get_db)):
    household = db.query(Household).filter(Household.id == appliance.household_id).first()
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")
    db_appliance = Appliance(**appliance.model_dump())
    db.add(db_appliance)
    db.commit()
    db.refresh(db_appliance)
    return db_appliance


@router.get("/", response_model=list[ApplianceResponse])
def list_appliances(household_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Appliance)
    if household_id:
        query = query.filter(Appliance.household_id == household_id)
    return query.all()


@router.get("/{appliance_id}", response_model=ApplianceResponse)
def get_appliance(appliance_id: int, db: Session = Depends(get_db)):
    appliance = db.query(Appliance).filter(Appliance.id == appliance_id).first()
    if not appliance:
        raise HTTPException(status_code=404, detail="Appliance not found")
    return appliance


@router.put("/{appliance_id}", response_model=ApplianceResponse)
def update_appliance(appliance_id: int, update: ApplianceUpdate, db: Session = Depends(get_db)):
    appliance = db.query(Appliance).filter(Appliance.id == appliance_id).first()
    if not appliance:
        raise HTTPException(status_code=404, detail="Appliance not found")
    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(appliance, field, value)
    db.commit()
    db.refresh(appliance)
    return appliance


@router.delete("/{appliance_id}", status_code=204)
def delete_appliance(appliance_id: int, db: Session = Depends(get_db)):
    appliance = db.query(Appliance).filter(Appliance.id == appliance_id).first()
    if not appliance:
        raise HTTPException(status_code=404, detail="Appliance not found")
    db.delete(appliance)
    db.commit()
