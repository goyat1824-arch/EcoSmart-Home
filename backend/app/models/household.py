from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base


class Household(Base):
    __tablename__ = "households"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200), nullable=False)
    address = Column(String(500))
    city = Column(String(100), default="Sceaux")
    latitude = Column(Float, default=48.78)
    longitude = Column(Float, default=2.29)
    tariff_per_kwh = Column(Float, default=0.174)  # EUR per kWh (France avg)
    emission_factor = Column(Float, default=0.055)  # kg CO2/kWh (France)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="households")
    appliances = relationship("Appliance", back_populates="household", cascade="all, delete-orphan")
    energy_readings = relationship("EnergyReading", back_populates="household", cascade="all, delete-orphan")
