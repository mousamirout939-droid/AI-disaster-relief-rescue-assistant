"""Business logic for shelters (CRUD + nearest-shelter lookup)."""
from typing import Any, Dict, List

from bson import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from schemas.shelter_schema import ShelterCreateRequest
from utils.helpers import serialize_mongo_doc
from utils.location import haversine_km, near_query


async def create_shelter(db: AsyncIOMotorDatabase, payload: ShelterCreateRequest) -> Dict[str, Any]:
    doc = {
        "name": payload.name,
        "location": {"type": "Point", "coordinates": [payload.lng, payload.lat]},
        "address": payload.address,
        "capacity": payload.capacity,
        "occupancy": 0,
        "resources": payload.resources,
        "contact_number": payload.contact_number,
        "status": "open",
    }
    result = await db["shelters"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_mongo_doc(doc)


async def list_shelters(db: AsyncIOMotorDatabase) -> List[Dict[str, Any]]:
    return [serialize_mongo_doc(doc) async for doc in db["shelters"].find({})]


async def find_nearby_shelters(db: AsyncIOMotorDatabase, lat: float, lng: float, radius_km: float = 15) -> List[Dict[str, Any]]:
    results = []
    async for doc in db["shelters"].find(near_query(lng, lat, radius_km)):
        item = serialize_mongo_doc(doc)
        coords = doc["location"]["coordinates"]
        item["distance_km"] = round(haversine_km(lat, lng, coords[1], coords[0]), 2)
        results.append(item)
    return sorted(results, key=lambda x: x["distance_km"])


async def update_shelter_occupancy(db: AsyncIOMotorDatabase, shelter_id: str, occupancy: int) -> Dict[str, Any]:
    if not ObjectId.is_valid(shelter_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid shelter id.")
    doc = await db["shelters"].find_one_and_update(
        {"_id": ObjectId(shelter_id)}, {"$set": {"occupancy": occupancy}}, return_document=True
    )
    if not doc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Shelter not found.")
    return serialize_mongo_doc(doc)
