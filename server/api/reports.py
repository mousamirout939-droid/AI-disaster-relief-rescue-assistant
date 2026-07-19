"""Routes for user-submitted disaster reports with optional image upload + AI analysis."""
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from motor.motor_asyncio import AsyncIOMotorDatabase

from controllers import report_controller
from database.connection import get_db
from dependencies.ai_dependency import get_yolo_service
from middleware.auth import get_current_user, require_roles
from schemas.report_schema import ReportCreateRequest, ReportStatusUpdateRequest
from services.ai_service import AIService
from services.yolo_service import YoloService
from utils.constants import DisasterType
from utils.response import success_response

router = APIRouter(prefix="/reports", tags=["Disaster Reports"])


@router.post("", response_model=None)
async def submit_report(
    disaster_type: DisasterType = Form(...),
    description: str = Form(...),
    lat: float = Form(...),
    lng: float = Form(...),
    address: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
    yolo: YoloService = Depends(get_yolo_service),
):
    payload = ReportCreateRequest(
        disaster_type=disaster_type, description=description, lat=lat, lng=lng, address=address
    )
    ai_service = AIService(yolo)
    data = await report_controller.create_report(db, current_user["id"], payload, image, ai_service)
    return success_response(data, "Report submitted successfully", 201)


@router.get("", response_model=None)
async def list_reports(
    page: int = 1, limit: int = 20, status: Optional[str] = None,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    data = await report_controller.list_reports(db, page, limit, status)
    return success_response(data, "Reports fetched")


@router.get("/mine", response_model=None)
async def my_reports(current_user: dict = Depends(get_current_user), db: AsyncIOMotorDatabase = Depends(get_db)):
    data = await report_controller.list_my_reports(db, current_user["id"])
    return success_response(data, "Your reports fetched")


@router.get("/{report_id}", response_model=None)
async def get_report(report_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    data = await report_controller.get_report(db, report_id)
    return success_response(data, "Report fetched")


@router.patch("/{report_id}/status", response_model=None)
async def update_report_status(
    report_id: str,
    payload: ReportStatusUpdateRequest,
    _admin=Depends(require_roles("admin")),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    data = await report_controller.update_report_status(db, report_id, payload.status.value)
    return success_response(data, "Report status updated")
