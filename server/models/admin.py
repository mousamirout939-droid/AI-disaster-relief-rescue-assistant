"""Admin document model. Kept separate from `users` collection for RBAC clarity."""
from typing import Optional

from pydantic import EmailStr, Field

from models.common import MongoBaseModel, utc_now


class AdminModel(MongoBaseModel):
    name: str
    email: EmailStr
    password: str  # hashed
    role: str = "admin"
    permissions: list[str] = Field(default_factory=lambda: ["manage_users", "manage_reports", "manage_resources"])
    is_active: bool = True
    created_at: float = Field(default_factory=lambda: utc_now().timestamp())
