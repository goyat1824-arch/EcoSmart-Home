from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.ml.predictor import predict_daily, predict_monthly, get_model_metrics

router = APIRouter()


@router.get("/daily")
def daily_prediction(
    household_id: int,
    days: int = Query(default=7, le=30),
    db: Session = Depends(get_db),
):
    try:
        return predict_daily(db, household_id, days)
    except FileNotFoundError:
        return {"error": "Model not trained yet. Run the training pipeline first."}
    except Exception as e:
        return {"error": str(e)}


@router.get("/monthly")
def monthly_prediction(household_id: int, db: Session = Depends(get_db)):
    try:
        return predict_monthly(db, household_id)
    except FileNotFoundError:
        return {"error": "Model not trained yet. Run the training pipeline first."}
    except Exception as e:
        return {"error": str(e)}


@router.get("/model-metrics")
def model_metrics():
    metrics = get_model_metrics()
    if metrics is None:
        return {"error": "No training results available. Train the model first."}
    return metrics
