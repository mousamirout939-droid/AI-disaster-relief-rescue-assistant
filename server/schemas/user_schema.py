"""Schemas for user profile read/update."""
from typing import Optional

from pydantic import BaseModel, EmailStr

from utils.constants import UserRole


class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: UserRole
    phone: Optional[str] = None
    profile_image: Optional[str] = None
    preferred_language: str = "en"
    is_active: bool = True
    is_verified: bool = False


class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    preferred_language: Optional[str] = None
