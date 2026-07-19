"""Volunteer registration document model."""
from typing import Optional

from pydantic import EmailStr, Field

from models.common import MongoBaseModel, utc_now


class VolunteerModel(MongoBaseModel):
    name: str
    email: EmailStr
    phone: str
    skills: list[str] = Field(default_factory=list)
    availability: str = "weekends"
    location: Optional[str] = None
    is_approved: bool = False
    created_at: float = Field(default_factory=lambda: utc_now().timestamp())
