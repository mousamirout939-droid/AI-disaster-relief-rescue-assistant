"""Rescue team document model."""
from typing import Optional

from pydantic import Field

from models.common import GeoPoint, MongoBaseModel, utc_now


class RescueTeamModel(MongoBaseModel):
    name: str
    team_lead: Optional[str] = None
    contact_number: Optional[str] = None
    members_count: int = 1
    specialization: str = "general"  # flood, fire, medical, search_rescue...
    location: GeoPoint
    status: str = "available"  # available | dispatched | off_duty
    assigned_report_id: Optional[str] = None
    created_at: float = Field(default_factory=lambda: utc_now().timestamp())
