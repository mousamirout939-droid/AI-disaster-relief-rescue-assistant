"""Schemas for classified disaster events."""
from typing import Optional

from pydantic import BaseModel

from utils.constants import DisasterType, SeverityLevel


class DisasterOut(BaseModel):
    id: str
    type: DisasterType
    severity: SeverityLevel
    description: Optional[str] = None
    status: str
    reported_count: int
    created_at: float


class LocationQuery(BaseModel):
    lat: float
    lng: float
    radius_km: float = 10
