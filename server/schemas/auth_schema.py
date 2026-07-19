"""Request/response schemas for authentication endpoints."""
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from utils.constants import UserRole
from utils.validators import is_strong_password


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str
    phone: Optional[str] = None
    role: UserRole = UserRole.USER

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not is_strong_password(v):
            raise ValueError("Password must be 8+ chars with upper, lower, and a digit.")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        if not is_strong_password(v):
            raise ValueError("Password must be 8+ chars with upper, lower, and a digit.")
        return v
