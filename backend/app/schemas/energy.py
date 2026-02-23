from pydantic import BaseModel
from datetime import date, datetime


class EnergyReadingCreate(BaseModel):
    household_id: int
    date: date
    total_kwh: float
    peak_hour: int | None = None
    sub_metering_kitchen: float = 0.0
    sub_metering_laundry: float = 0.0
    sub_metering_hvac: float = 0.0
    global_active_power_avg: float | None = None
    voltage_avg: float | None = None


class EnergyReadingResponse(BaseModel):
    id: int
    household_id: int
    date: date
    total_kwh: float
    peak_hour: int | None
    sub_metering_kitchen: float
    sub_metering_laundry: float
    sub_metering_hvac: float
    global_active_power_avg: float | None
    voltage_avg: float | None
    created_at: datetime

    model_config = {"from_attributes": True}
