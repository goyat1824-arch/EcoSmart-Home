from pydantic import BaseModel
from datetime import datetime


class HouseholdCreate(BaseModel):
    user_id: int
    name: str
    address: str | None = None
    city: str = "Sceaux"
    latitude: float = 48.78
    longitude: float = 2.29
    tariff_per_kwh: float = 0.174
    emission_factor: float = 0.055


class HouseholdUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    tariff_per_kwh: float | None = None
    emission_factor: float | None = None


class HouseholdResponse(BaseModel):
    id: int
    user_id: int
    name: str
    address: str | None
    city: str
    latitude: float
    longitude: float
    tariff_per_kwh: float
    emission_factor: float
    created_at: datetime

    model_config = {"from_attributes": True}
