"""Business logic for registration, login, token refresh, and password management."""
from typing import Any, Dict

from bson import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from config.jwt_handler import create_access_token, create_refresh_token, decode_token
from config.security import hash_password, verify_password
from schemas.auth_schema import ChangePasswordRequest, LoginRequest, RegisterRequest
from utils.constants import UserRole
from utils.helpers import now_ts, serialize_mongo_doc


async def register_user(db: AsyncIOMotorDatabase, payload: RegisterRequest) -> Dict[str, Any]:
    existing = await db["users"].find_one({"email": payload.email})
    if existing:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "An account with this email already exists.")

    doc = {
        "name": payload.name,
        "email": payload.email,
        "password": hash_password(payload.password),
        "role": payload.role.value,
        "phone": payload.phone,
        "is_active": True,
        "is_verified": False,
        "created_at": now_ts(),
    }
    result = await db["users"].insert_one(doc)
    return _issue_tokens(str(result.inserted_id), payload.role.value)


async def login_user(db: AsyncIOMotorDatabase, payload: LoginRequest) -> Dict[str, Any]:
    user = await db["users"].find_one({"email": payload.email})
    collection_role = "user"

    if not user:
        user = await db["admins"].find_one({"email": payload.email})
        collection_role = "admin"

    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password.")

    if not user.get("is_active", True):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "This account has been deactivated.")

    role = user.get("role", collection_role)
    return _issue_tokens(str(user["_id"]), role)


async def refresh_access_token(refresh_token: str) -> Dict[str, str]:
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired refresh token.")

    new_access = create_access_token({"sub": payload["sub"], "role": payload.get("role", "user")})
    return {"access_token": new_access, "token_type": "bearer"}


async def change_password(db: AsyncIOMotorDatabase, current_user: Dict[str, Any], payload: ChangePasswordRequest) -> None:
    collection = "admins" if current_user.get("role") == "admin" else "users"
    user = await db[collection].find_one({"_id": ObjectId(current_user["id"])})

    if not user or not verify_password(payload.old_password, user["password"]):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Old password is incorrect.")

    await db[collection].update_one(
        {"_id": ObjectId(current_user["id"])},
        {"$set": {"password": hash_password(payload.new_password)}},
    )


def _issue_tokens(user_id: str, role: str) -> Dict[str, str]:
    token_data = {"sub": user_id, "role": role}
    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
        "token_type": "bearer",
    }
