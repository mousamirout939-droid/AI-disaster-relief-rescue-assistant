"""SOS trigger + emergency contacts routes. (Not in the original skeleton's api/
folder listing, added because SOS Button and Emergency Contacts are both
explicitly required features.)"""
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel, Field

from database.connection import get_db
from middleware.auth import get_current_user
from services.emergency_service import EmergencyService
from utils.helpers import serialize_mongo_doc
from utils.response import success_response

router = APIRouter(prefix="/emergency", tags=["Emergency"])


class SOSRequest(BaseModel):
    lat: float
    lng: float


class EmergencyContactRequest(BaseModel):
    name: str
    phone: str
    relation: Optional[str] = None


@router.post("/sos", response_model=None)
async def trigger_sos(
    payload: SOSRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    service = EmergencyService(db)
    result = await service.trigger_sos(current_user["id"], payload.lat, payload.lng)
    return success_response(result, "SOS triggered — help is being located.")


@router.get("/contacts", response_model=None)
async def list_contacts(current_user: dict = Depends(get_current_user), db: AsyncIOMotorDatabase = Depends(get_db)):
    cursor = db["emergency_contacts"].find({"user_id": current_user["id"]})
    data = [serialize_mongo_doc(doc) async for doc in cursor]
    return success_response(data, "Emergency contacts fetched")


@router.post("/contacts", response_model=None)
async def add_contact(
    payload: EmergencyContactRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    doc = payload.model_dump()
    doc["user_id"] = current_user["id"]
    result = await db["emergency_contacts"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return success_response(serialize_mongo_doc(doc), "Emergency contact added", 201)


@router.delete("/contacts/{contact_id}", response_model=None)
async def delete_contact(
    contact_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    if ObjectId.is_valid(contact_id):
        await db["emergency_contacts"].delete_one({"_id": ObjectId(contact_id), "user_id": current_user["id"]})
    return success_response(None, "Emergency contact removed")
