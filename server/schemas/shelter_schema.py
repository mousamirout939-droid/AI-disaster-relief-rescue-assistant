"""Schemas for shelters."""
from typing import Optional

from pydantic import BaseModel, Field


class ShelterCreateRequest(BaseModel):
    name: str
    lat: float
    lng: float
    address: Optional[str] = None
    capacity: int = 0
    resources: list[str] = Field(default_factory=list)
    contact_number: Optional[str] = None


class ShelterOut(BaseModel):
    id: str
    name: str
    address: Optional[str] = None
    capacity: int
    occupancy: int
    resources: list[str]
    status: str
    distance_km: Optional[float] = None
