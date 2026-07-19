"""Routes for in-app notifications."""
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from controllers import notification_controller
from database.connection import get_db
from middleware.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=None)
async def list_notifications(current_user: dict = Depends(get_current_user), db: AsyncIOMotorDatabase = Depends(get_db)):
    data = await notification_controller.list_notifications(db, current_user["id"])
    return success_response(data, "Notifications fetched")


@router.patch("/{notification_id}/read", response_model=None)
async def mark_read(notification_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    await notification_controller.mark_as_read(db, notification_id)
    return success_response(None, "Notification marked as read")
