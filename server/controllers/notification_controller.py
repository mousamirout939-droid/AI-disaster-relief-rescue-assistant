"""Business logic for reading/creating in-app notifications."""
from typing import Any, Dict, List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from utils.helpers import serialize_mongo_doc


async def list_notifications(db: AsyncIOMotorDatabase, user_id: str) -> List[Dict[str, Any]]:
    query = {"$or": [{"user_id": user_id}, {"user_id": None}]}
    cursor = db["notifications"].find(query).sort("created_at", -1).limit(50)
    return [serialize_mongo_doc(doc) async for doc in cursor]


async def mark_as_read(db: AsyncIOMotorDatabase, notification_id: str) -> None:
    if ObjectId.is_valid(notification_id):
        await db["notifications"].update_one({"_id": ObjectId(notification_id)}, {"$set": {"read": True}})
