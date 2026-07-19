"""Admin dashboard business logic: aggregate stats, user management."""
from typing import Any, Dict, List

from bson import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from utils.helpers import serialize_mongo_doc


async def get_dashboard_stats(db: AsyncIOMotorDatabase) -> Dict[str, Any]:
    return {
        "total_users": await db["users"].count_documents({}),
        "total_reports": await db["disaster_reports"].count_documents({}),
        "pending_reports": await db["disaster_reports"].count_documents({"status": "pending"}),
        "active_disasters": await db["disasters"].count_documents({"status": "active"}),
        "total_shelters": await db["shelters"].count_documents({}),
        "total_hospitals": await db["hospitals"].count_documents({}),
        "rescue_teams_available": await db["rescue_teams"].count_documents({"status": "available"}),
        "rescue_teams_dispatched": await db["rescue_teams"].count_documents({"status": "dispatched"}),
        "pending_volunteers": await db["volunteers"].count_documents({"is_approved": False}),
    }


async def list_users(db: AsyncIOMotorDatabase) -> List[Dict[str, Any]]:
    users = [serialize_mongo_doc(doc) async for doc in db["users"].find({}, {"password": 0})]
    return users


async def set_user_active(db: AsyncIOMotorDatabase, user_id: str, is_active: bool) -> Dict[str, Any]:
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid user id.")
    doc = await db["users"].find_one_and_update(
        {"_id": ObjectId(user_id)}, {"$set": {"is_active": is_active}}, return_document=True
    )
    if not doc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found.")
    doc.pop("password", None)
    return serialize_mongo_doc(doc)
