"""Volunteer registration routes. (Added alongside emergency.py for the same reason.)"""
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from database.connection import get_db
from middleware.auth import require_roles
from utils.helpers import now_ts, serialize_mongo_doc
from utils.response import success_response
from schemas.user_schema import UserOut  # noqa: F401  (kept for symmetry with other schema imports)
from pydantic import BaseModel, EmailStr, Field

router = APIRouter(prefix="/volunteers", tags=["Volunteers"])


class VolunteerRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    skills: list[str] = Field(default_factory=list)
    availability: str = "weekends"
    location: str | None = None


@router.post("", response_model=None)
async def register_volunteer(payload: VolunteerRegisterRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    doc = payload.model_dump()
    doc.update({"is_approved": False, "created_at": now_ts()})
    result = await db["volunteers"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return success_response(serialize_mongo_doc(doc), "Volunteer registration submitted", 201)


@router.get("", response_model=None)
async def list_volunteers(_admin=Depends(require_roles("admin")), db: AsyncIOMotorDatabase = Depends(get_db)):
    data = [serialize_mongo_doc(doc) async for doc in db["volunteers"].find({})]
    return success_response(data, "Volunteers fetched")


@router.patch("/{volunteer_id}/approve", response_model=None)
async def approve_volunteer(volunteer_id: str, _admin=Depends(require_roles("admin")), db: AsyncIOMotorDatabase = Depends(get_db)):
    from bson import ObjectId
    doc = await db["volunteers"].find_one_and_update(
        {"_id": ObjectId(volunteer_id)}, {"$set": {"is_approved": True}}, return_document=True
    )
    return success_response(serialize_mongo_doc(doc) if doc else None, "Volunteer approved")
