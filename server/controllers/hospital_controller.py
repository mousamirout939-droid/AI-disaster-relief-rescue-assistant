"""Business logic for hospitals (CRUD + nearest-hospital lookup)."""
from typing import Any, Dict, List

from motor.motor_asyncio import AsyncIOMotorDatabase

from schemas.hospital_schema import HospitalCreateRequest
from utils.helpers import serialize_mongo_doc
from utils.location import haversine_km, near_query


async def create_hospital(db: AsyncIOMotorDatabase, payload: HospitalCreateRequest) -> Dict[str, Any]:
    doc = {
        "name": payload.name,
        "location": {"type": "Point", "coordinates": [payload.lng, payload.lat]},
        "address": payload.address,
        "beds_available": payload.beds_available,
        "specialities": payload.specialities,
        "contact_number": payload.contact_number,
        "is_emergency_capable": True,
    }
    result = await db["hospitals"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_mongo_doc(doc)


async def list_hospitals(db: AsyncIOMotorDatabase) -> List[Dict[str, Any]]:
    return [serialize_mongo_doc(doc) async for doc in db["hospitals"].find({})]


async def find_nearby_hospitals(db: AsyncIOMotorDatabase, lat: float, lng: float, radius_km: float = 15) -> List[Dict[str, Any]]:
    results = []
    async for doc in db["hospitals"].find(near_query(lng, lat, radius_km)):
        item = serialize_mongo_doc(doc)
        coords = doc["location"]["coordinates"]
        item["distance_km"] = round(haversine_km(lat, lng, coords[1], coords[0]), 2)
        results.append(item)
    return sorted(results, key=lambda x: x["distance_km"])
