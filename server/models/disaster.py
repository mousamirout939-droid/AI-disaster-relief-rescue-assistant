"""Disaster event model — an aggregated/classified disaster (distinct from a raw user report)."""
from typing import Optional

from pydantic import Field

from models.common import GeoPoint, MongoBaseModel, utc_now
from utils.constants import DisasterType, SeverityLevel


class DisasterModel(MongoBaseModel):
    type: DisasterType
    severity: SeverityLevel
    description: Optional[str] = None
    location: GeoPoint
    affected_radius_km: float = 1.0
    reported_count: int = 1
    status: str = "active"  # active | contained | resolved
    created_at: float = Field(default_factory=lambda: utc_now().timestamp())
    updated_at: Optional[float] = None
