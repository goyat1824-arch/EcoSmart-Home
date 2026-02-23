from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from datetime import datetime, timezone

from app.database import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    city = Column(String(100), default="Sceaux")
    avg_temp = Column(Float)  # Celsius
    min_temp = Column(Float)
    max_temp = Column(Float)
    humidity = Column(Float)  # %
    wind_speed = Column(Float)  # km/h
    precipitation = Column(Float, default=0.0)  # mm
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
