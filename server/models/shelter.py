"""Shelter document model."""
from typing import Optional

from pydantic import Field

from models.common import GeoPoint, MongoBaseModel, utc_now


class ShelterModel(MongoBaseModel):
    name: str
    location: GeoPoint
    address: Optional[str] = None
    capacity: int = 0
    occupancy: int = 0
    resources: list[str] = Field(default_factory=list)
    contact_number: Optional[str] = None
    status: str = "open"  # open | full | closed
    created_at: float = Field(default_factory=lambda: utc_now().timestamp())
