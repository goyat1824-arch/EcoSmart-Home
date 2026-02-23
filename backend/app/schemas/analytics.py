from pydantic import BaseModel
from datetime import date


class CO2Response(BaseModel):
    date: date
    energy_kwh: float
    co2_kg: float
    emission_factor: float


class CostResponse(BaseModel):
    date: date
    energy_kwh: float
    cost: float
    tariff: float


class SustainabilityScore(BaseModel):
    household_id: int
    score: float  # 0-100
    grade: str  # A, B, C, D, F
    avg_daily_kwh: float
    baseline_daily_kwh: float
    trend: str  # improving, stable, declining
    co2_saved_kg: float


class DashboardSummary(BaseModel):
    today_kwh: float
    yesterday_kwh: float
    daily_change_pct: float
    monthly_kwh: float
    monthly_cost: float
    monthly_co2_kg: float
    sustainability_score: float
    sustainability_grade: str
    predicted_tomorrow_kwh: float
    avg_daily_kwh_7d: float


class PredictionResponse(BaseModel):
    date: date
    predicted_kwh: float
    confidence_lower: float
    confidence_upper: float


class RecommendationResponse(BaseModel):
    id: int
    category: str  # efficiency, behavior, upgrade, scheduling
    title: str
    description: str
    potential_savings_kwh: float
    potential_savings_cost: float
    priority: str  # high, medium, low
