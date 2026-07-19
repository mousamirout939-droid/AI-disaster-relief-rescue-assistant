"""Hospital document model."""
from typing import Optional

from pydantic import Field

from models.common import GeoPoint, MongoBaseModel, utc_now


class HospitalModel(MongoBaseModel):
    name: str
    location: GeoPoint
    address: Optional[str] = None
    contact_number: Optional[str] = None
    beds_available: int = 0
    specialities: list[str] = Field(default_factory=list)
    is_emergency_capable: bool = True
    created_at: float = Field(default_factory=lambda: utc_now().timestamp())
