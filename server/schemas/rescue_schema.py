"""Schemas for rescue teams."""
from typing import Optional

from pydantic import BaseModel


class RescueTeamCreateRequest(BaseModel):
    name: str
    team_lead: Optional[str] = None
    contact_number: Optional[str] = None
    members_count: int = 1
    specialization: str = "general"
    lat: float
    lng: float


class RescueTeamOut(BaseModel):
    id: str
    name: str
    specialization: str
    status: str
    members_count: int
    distance_km: Optional[float] = None


class DispatchRequest(BaseModel):
    report_id: str
