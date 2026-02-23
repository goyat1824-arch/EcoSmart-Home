from sqlalchemy import Column, Integer, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base


class EnergyReading(Base):
    __tablename__ = "energy_readings"

    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    total_kwh = Column(Float, nullable=False)
    peak_hour = Column(Integer)  # 0-23
    sub_metering_kitchen = Column(Float, default=0.0)  # kWh
    sub_metering_laundry = Column(Float, default=0.0)  # kWh
    sub_metering_hvac = Column(Float, default=0.0)  # kWh
    global_active_power_avg = Column(Float)  # kW average for the day
    voltage_avg = Column(Float)  # Voltage average
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    household = relationship("Household", back_populates="energy_readings")
