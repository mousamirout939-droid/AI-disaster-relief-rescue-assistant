"""Business logic for listing/creating classified disaster events."""
from typing import Any, Dict, List

from bson import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from models.common import GeoPoint
from models.disaster import DisasterModel
from utils.helpers import serialize_mongo_doc
from utils.location import near_query


async def list_disasters(db: AsyncIOMotorDatabase, status_filter: str | None = None) -> List[Dict[str, Any]]:
    query = {"status": status_filter} if status_filter else {}
    cursor = db["disasters"].find(query).sort("created_at", -1)
    return [serialize_mongo_doc(doc) async for doc in cursor]


async def get_disasters_near(db: AsyncIOMotorDatabase, lat: float, lng: float, radius_km: float) -> List[Dict[str, Any]]:
    cursor = db["disasters"].find(near_query(lng, lat, radius_km))
    return [serialize_mongo_doc(doc) async for doc in cursor]


async def create_disaster(db: AsyncIOMotorDatabase, disaster: DisasterModel) -> Dict[str, Any]:
    doc = disaster.model_dump(exclude={"id"}, exclude_none=True)
    result = await db["disasters"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_mongo_doc(doc)


async def update_disaster_status(db: AsyncIOMotorDatabase, disaster_id: str, new_status: str) -> Dict[str, Any]:
    if not ObjectId.is_valid(disaster_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid disaster id.")

    result = await db["disasters"].find_one_and_update(
        {"_id": ObjectId(disaster_id)},
        {"$set": {"status": new_status}},
        return_document=True,
    )
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Disaster not found.")
    return serialize_mongo_doc(result)
