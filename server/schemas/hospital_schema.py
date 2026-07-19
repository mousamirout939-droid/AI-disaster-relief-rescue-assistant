"""Schemas for hospitals."""
from typing import Optional

from pydantic import BaseModel, Field


class HospitalCreateRequest(BaseModel):
    name: str
    lat: float
    lng: float
    address: Optional[str] = None
    beds_available: int = 0
    specialities: list[str] = Field(default_factory=list)
    contact_number: Optional[str] = None


class HospitalOut(BaseModel):
    id: str
    name: str
    address: Optional[str] = None
    beds_available: int
    specialities: list[str]
    distance_km: Optional[float] = None
