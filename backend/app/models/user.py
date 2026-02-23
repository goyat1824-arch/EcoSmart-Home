from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    country = Column(String(100), default="India")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    households = relationship("Household", back_populates="user", cascade="all, delete-orphan")
