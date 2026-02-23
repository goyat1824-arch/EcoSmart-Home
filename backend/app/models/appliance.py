from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base


class Appliance(Base):
    __tablename__ = "appliances"

    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)  # Kitchen, Laundry, HVAC, Lighting, Other
    watt_rating = Column(Float, nullable=False)
    avg_usage_hours = Column(Float, default=0.0)
    efficiency_rating = Column(Integer, default=3)  # 1-5 stars
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    household = relationship("Household", back_populates="appliances")
