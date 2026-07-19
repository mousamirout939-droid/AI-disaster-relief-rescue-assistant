"""
JWT bearer authentication. `get_current_user` is the core dependency every
protected route uses; `require_roles` builds role-gated variants of it.
"""
from typing import Any, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorDatabase

from bson import ObjectId
from config.jwt_handler import decode_token
from database.connection import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login", auto_error=False)

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> Dict[str, Any]:
    if not token:
        raise CREDENTIALS_EXCEPTION

    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise CREDENTIALS_EXCEPTION

    user_id = payload.get("sub")
    role = payload.get("role", "user")
    collection = "admins" if role == "admin" else "users"

    if not user_id or not ObjectId.is_valid(user_id):
        raise CREDENTIALS_EXCEPTION

    user = await db[collection].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise CREDENTIALS_EXCEPTION

    user["id"] = str(user.pop("_id"))
    user.setdefault("role", role)
    return user


def require_roles(*allowed_roles: str):
    """Usage: Depends(require_roles("admin")) or Depends(require_roles("admin", "rescue_team"))."""

    async def role_checker(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        if current_user.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )
        return current_user

    return role_checker
