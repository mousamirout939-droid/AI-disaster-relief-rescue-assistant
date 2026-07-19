"""Schemas for weather/disaster alerts."""
from typing import Optional

from pydantic import BaseModel

from utils.constants import SeverityLevel


class AlertCreateRequest(BaseModel):
    title: str
    message: str
    severity: SeverityLevel
    region: Optional[str] = None


class AlertOut(BaseModel):
    id: str
    title: str
    message: str
    severity: SeverityLevel
    region: Optional[str] = None
    active: bool
    created_at: float
