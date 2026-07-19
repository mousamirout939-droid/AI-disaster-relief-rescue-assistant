"""User-submitted disaster report, optionally with an uploaded image analyzed by YOLO."""
from typing import Optional

from pydantic import Field

from models.common import GeoPoint, MongoBaseModel, utc_now
from utils.constants import DisasterType, ReportStatus, SeverityLevel


class DisasterReportModel(MongoBaseModel):
    user_id: str
    disaster_type: DisasterType
    description: str
    location: GeoPoint
    address: Optional[str] = None
    image_url: Optional[str] = None
    ai_detections: list[dict] = Field(default_factory=list)   # YOLO output boxes/classes
    ai_severity: Optional[SeverityLevel] = None
    ai_confidence: Optional[float] = None
    status: ReportStatus = ReportStatus.PENDING
    verified_by_admin: bool = False
    created_at: float = Field(default_factory=lambda: utc_now().timestamp())
    updated_at: Optional[float] = None
