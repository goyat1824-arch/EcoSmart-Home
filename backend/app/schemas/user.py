from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: str
    country: str = "India"


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    country: str
    created_at: datetime

    model_config = {"from_attributes": True}
