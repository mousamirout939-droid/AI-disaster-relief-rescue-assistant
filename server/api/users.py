"""User profile routes."""
from bson import ObjectId
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from database.connection import get_db
from middleware.auth import get_current_user
from schemas.user_schema import UserUpdateRequest
from utils.helpers import serialize_mongo_doc
from utils.response import success_response

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/profile", response_model=None)
async def get_profile(current_user: dict = Depends(get_current_user)):
    current_user.pop("password", None)
    return success_response(current_user, "Profile fetched")


@router.put("/profile", response_model=None)
async def update_profile(
    payload: UserUpdateRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    if updates:
        await db["users"].update_one({"_id": ObjectId(current_user["id"])}, {"$set": updates})
    doc = await db["users"].find_one({"_id": ObjectId(current_user["id"])})
    doc.pop("password", None)
    return success_response(serialize_mongo_doc(doc), "Profile updated")
