"""Weather / disaster alert broadcast model."""
from typing import Optional

from pydantic import Field

from models.common import GeoPoint, MongoBaseModel, utc_now
from utils.constants import SeverityLevel


class AlertModel(MongoBaseModel):
    title: str
    message: str
    severity: SeverityLevel
    region: Optional[str] = None
    location: Optional[GeoPoint] = None
    source: str = "system"  # system | weather_api | admin
    active: bool = True
    created_at: float = Field(default_factory=lambda: utc_now().timestamp())
