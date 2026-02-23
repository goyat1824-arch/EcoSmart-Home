from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.recommendation_service import get_recommendations

router = APIRouter()


@router.get("/")
def recommendations(household_id: int, db: Session = Depends(get_db)):
    return get_recommendations(db, household_id)
