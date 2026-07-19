"""Admin dashboard routes."""
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from controllers import admin_controller
from database.connection import get_db
from middleware.auth import require_roles
from utils.response import success_response

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(require_roles("admin"))])


@router.get("/dashboard", response_model=None)
async def dashboard_stats(db: AsyncIOMotorDatabase = Depends(get_db)):
    data = await admin_controller.get_dashboard_stats(db)
    return success_response(data, "Dashboard stats fetched")


@router.get("/users", response_model=None)
async def users(db: AsyncIOMotorDatabase = Depends(get_db)):
    data = await admin_controller.list_users(db)
    return success_response(data, "Users fetched")


@router.patch("/users/{user_id}/active", response_model=None)
async def set_active(user_id: str, is_active: bool, db: AsyncIOMotorDatabase = Depends(get_db)):
    data = await admin_controller.set_user_active(db, user_id, is_active)
    return success_response(data, "User status updated")
