"""Business logic for user-submitted disaster reports, including AI analysis."""
from typing import Any, Dict, List, Optional

from bson import ObjectId
from fastapi import HTTPException, UploadFile, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from schemas.report_schema import ReportCreateRequest
from services.ai_service import AIService
from utils.file_upload import save_upload_file
from utils.helpers import now_ts, serialize_mongo_doc
from utils.helpers import paginate

BASE_DIR = __import__("pathlib").Path(__file__).resolve().parent.parent


async def create_report(
    db: AsyncIOMotorDatabase,
    user_id: str,
    payload: ReportCreateRequest,
    image: Optional[UploadFile],
    ai_service: AIService,
) -> Dict[str, Any]:
    doc: Dict[str, Any] = {
        "user_id": user_id,
        "disaster_type": payload.disaster_type.value,
        "description": payload.description,
        "location": {"type": "Point", "coordinates": [payload.lng, payload.lat]},
        "address": payload.address,
        "image_url": None,
        "ai_detections": [],
        "ai_severity": None,
        "ai_confidence": None,
        "status": "pending",
        "verified_by_admin": False,
        "created_at": now_ts(),
    }

    if image is not None:
        relative_url = await save_upload_file(image, subfolder="disaster_images")
        doc["image_url"] = relative_url

        absolute_path = str(BASE_DIR / relative_url.lstrip("/"))
        analysis = ai_service.analyze_report_image(absolute_path)
        doc["ai_detections"] = analysis["detections"]
        doc["ai_severity"] = analysis["severity"].value
        doc["ai_confidence"] = analysis["confidence"]

    result = await db["disaster_reports"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_mongo_doc(doc)


async def list_reports(db: AsyncIOMotorDatabase, page: int = 1, limit: int = 20, status_filter: str | None = None) -> List[Dict[str, Any]]:
    skip, limit = paginate({"page": page, "limit": limit})
    query = {"status": status_filter} if status_filter else {}
    cursor = db["disaster_reports"].find(query).sort("created_at", -1).skip(skip).limit(limit)
    return [serialize_mongo_doc(doc) async for doc in cursor]


async def get_report(db: AsyncIOMotorDatabase, report_id: str) -> Dict[str, Any]:
    if not ObjectId.is_valid(report_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid report id.")
    doc = await db["disaster_reports"].find_one({"_id": ObjectId(report_id)})
    if not doc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Report not found.")
    return serialize_mongo_doc(doc)


async def update_report_status(db: AsyncIOMotorDatabase, report_id: str, new_status: str) -> Dict[str, Any]:
    if not ObjectId.is_valid(report_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid report id.")
    doc = await db["disaster_reports"].find_one_and_update(
        {"_id": ObjectId(report_id)},
        {"$set": {"status": new_status, "verified_by_admin": True}},
        return_document=True,
    )
    if not doc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Report not found.")
    return serialize_mongo_doc(doc)


async def list_my_reports(db: AsyncIOMotorDatabase, user_id: str) -> List[Dict[str, Any]]:
    cursor = db["disaster_reports"].find({"user_id": user_id}).sort("created_at", -1)
    return [serialize_mongo_doc(doc) async for doc in cursor]
