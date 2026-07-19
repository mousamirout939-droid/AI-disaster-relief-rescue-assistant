"""Routes for disaster/weather alerts."""
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from database.connection import get_db
from middleware.auth import require_roles
from schemas.alert_schema import AlertCreateRequest
from utils.helpers import now_ts, serialize_mongo_doc
from utils.response import success_response

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=None)
async def list_alerts(db: AsyncIOMotorDatabase = Depends(get_db)):
    cursor = db["alerts"].find({"active": True}).sort("created_at", -1)
    data = [serialize_mongo_doc(doc) async for doc in cursor]
    return success_response(data, "Alerts fetched")


@router.post("", response_model=None)
async def create_alert(
    payload: AlertCreateRequest,
    _admin=Depends(require_roles("admin")),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    doc = payload.model_dump()
    doc.update({"active": True, "source": "admin", "created_at": now_ts()})
    result = await db["alerts"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return success_response(serialize_mongo_doc(doc), "Alert created", 201)
