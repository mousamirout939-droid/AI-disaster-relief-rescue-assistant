"""Shared enums and constants used across the backend."""
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    VOLUNTEER = "volunteer"
    RESCUE_TEAM = "rescue_team"
    ADMIN = "admin"


class DisasterType(str, Enum):
    FLOOD = "flood"
    FIRE = "fire"
    EARTHQUAKE = "earthquake"
    CYCLONE = "cyclone"
    TSUNAMI = "tsunami"
    LANDSLIDE = "landslide"
    BUILDING_DAMAGE = "building_damage"
    OTHER = "other"


class SeverityLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class ReportStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    REJECTED = "rejected"


class NotificationType(str, Enum):
    ALERT = "alert"
    REPORT_UPDATE = "report_update"
    SYSTEM = "system"
    SOS = "sos"


SEVERITY_ORDER = {
    SeverityLevel.LOW: 1,
    SeverityLevel.MODERATE: 2,
    SeverityLevel.HIGH: 3,
    SeverityLevel.CRITICAL: 4,
}
