"""User document model (role: user | volunteer | rescue_team | admin handled separately in admin.py)."""
from typing import Optional

from pydantic import EmailStr, Field

from models.common import MongoBaseModel, utc_now
from utils.constants import UserRole


class UserModel(MongoBaseModel):
    name: str
    email: EmailStr
    password: str  # hashed
    role: UserRole = UserRole.USER
    phone: Optional[str] = None
    profile_image: Optional[str] = None
    preferred_language: str = "en"
    is_active: bool = True
    is_verified: bool = False
    created_at: float = Field(default_factory=lambda: utc_now().timestamp())
    updated_at: Optional[float] = None
