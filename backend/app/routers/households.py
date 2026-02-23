from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.household import Household
from app.models.user import User
from app.schemas.household import HouseholdCreate, HouseholdUpdate, HouseholdResponse

router = APIRouter()


@router.post("/", response_model=HouseholdResponse, status_code=201)
def create_household(household: HouseholdCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == household.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_household = Household(**household.model_dump())
    db.add(db_household)
    db.commit()
    db.refresh(db_household)
    return db_household


@router.get("/", response_model=list[HouseholdResponse])
def list_households(user_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Household)
    if user_id:
        query = query.filter(Household.user_id == user_id)
    return query.all()


@router.get("/{household_id}", response_model=HouseholdResponse)
def get_household(household_id: int, db: Session = Depends(get_db)):
    household = db.query(Household).filter(Household.id == household_id).first()
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")
    return household


@router.put("/{household_id}", response_model=HouseholdResponse)
def update_household(household_id: int, update: HouseholdUpdate, db: Session = Depends(get_db)):
    household = db.query(Household).filter(Household.id == household_id).first()
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")
    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(household, field, value)
    db.commit()
    db.refresh(household)
    return household


@router.delete("/{household_id}", status_code=204)
def delete_household(household_id: int, db: Session = Depends(get_db)):
    household = db.query(Household).filter(Household.id == household_id).first()
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")
    db.delete(household)
    db.commit()
