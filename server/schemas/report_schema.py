"""Schemas for user-submitted disaster reports."""
from typing import Optional

from pydantic import BaseModel, Field

from utils.constants import DisasterType, ReportStatus, SeverityLevel


class ReportCreateRequest(BaseModel):
    disaster_type: DisasterType
    description: str = Field(min_length=5, max_length=1000)
    lat: float
    lng: float
    address: Optional[str] = None


class ReportOut(BaseModel):
    id: str
    user_id: str
    disaster_type: DisasterType
    description: str
    address: Optional[str] = None
    image_url: Optional[str] = None
    ai_severity: Optional[SeverityLevel] = None
    ai_confidence: Optional[float] = None
    status: ReportStatus
    created_at: float


class ReportStatusUpdateRequest(BaseModel):
    status: ReportStatus
