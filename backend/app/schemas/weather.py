from pydantic import BaseModel
from datetime import date


class WeatherResponse(BaseModel):
    id: int
    date: date
    city: str
    avg_temp: float | None
    min_temp: float | None
    max_temp: float | None
    humidity: float | None
    wind_speed: float | None
    precipitation: float

    model_config = {"from_attributes": True}
