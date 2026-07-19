"""Business logic for rescue teams (CRUD, nearest lookup, dispatch)."""
from typing import Any, Dict, List

from bson import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from schemas.rescue_schema import RescueTeamCreateRequest
from utils.helpers import serialize_mongo_doc
from utils.location import haversine_km, near_query


async def create_rescue_team(db: AsyncIOMotorDatabase, payload: RescueTeamCreateRequest) -> Dict[str, Any]:
    doc = {
        "name": payload.name,
        "team_lead": payload.team_lead,
        "contact_number": payload.contact_number,
        "members_count": payload.members_count,
        "specialization": payload.specialization,
        "location": {"type": "Point", "coordinates": [payload.lng, payload.lat]},
        "status": "available",
        "assigned_report_id": None,
    }
    result = await db["rescue_teams"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_mongo_doc(doc)


async def list_rescue_teams(db: AsyncIOMotorDatabase) -> List[Dict[str, Any]]:
    return [serialize_mongo_doc(doc) async for doc in db["rescue_teams"].find({})]


async def find_nearby_rescue_teams(db: AsyncIOMotorDatabase, lat: float, lng: float, radius_km: float = 25) -> List[Dict[str, Any]]:
    results = []
    query = {**near_query(lng, lat, radius_km), "status": "available"}
    async for doc in db["rescue_teams"].find(query):
        item = serialize_mongo_doc(doc)
        coords = doc["location"]["coordinates"]
        item["distance_km"] = round(haversine_km(lat, lng, coords[1], coords[0]), 2)
        results.append(item)
    return sorted(results, key=lambda x: x["distance_km"])


async def dispatch_team(db: AsyncIOMotorDatabase, team_id: str, report_id: str) -> Dict[str, Any]:
    if not ObjectId.is_valid(team_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid team id.")
    doc = await db["rescue_teams"].find_one_and_update(
        {"_id": ObjectId(team_id), "status": "available"},
        {"$set": {"status": "dispatched", "assigned_report_id": report_id}},
        return_document=True,
    )
    if not doc:
        raise HTTPException(status.HTTP_409_CONFLICT, "Team not found or already dispatched.")
    return serialize_mongo_doc(doc)
