from pydantic import BaseModel, Field
from datetime import datetime


class ApplianceCreate(BaseModel):
    household_id: int
    name: str
    category: str  # Kitchen, Laundry, HVAC, Lighting, Other
    watt_rating: float
    avg_usage_hours: float = 0.0
    efficiency_rating: int = Field(default=3, ge=1, le=5)


class ApplianceUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    watt_rating: float | None = None
    avg_usage_hours: float | None = None
    efficiency_rating: int | None = Field(default=None, ge=1, le=5)


class ApplianceResponse(BaseModel):
    id: int
    household_id: int
    name: str
    category: str
    watt_rating: float
    avg_usage_hours: float
    efficiency_rating: int
    created_at: datetime

    model_config = {"from_attributes": True}
