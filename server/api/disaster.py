"""Routes for classified disaster events."""
from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from controllers import disaster_controller
from database.connection import get_db
from middleware.auth import require_roles
from utils.response import success_response

router = APIRouter(prefix="/disasters", tags=["Disasters"])


@router.get("", response_model=None)
async def list_disasters(status: str | None = None, db: AsyncIOMotorDatabase = Depends(get_db)):
    data = await disaster_controller.list_disasters(db, status)
    return success_response(data, "Disasters fetched")


@router.get("/nearby", response_model=None)
async def nearby_disasters(
    lat: float = Query(...), lng: float = Query(...), radius_km: float = Query(10),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    data = await disaster_controller.get_disasters_near(db, lat, lng, radius_km)
    return success_response(data, "Nearby disasters fetched")


@router.patch("/{disaster_id}/status", response_model=None)
async def update_status(
    disaster_id: str,
    new_status: str,
    _admin=Depends(require_roles("admin")),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    data = await disaster_controller.update_disaster_status(db, disaster_id, new_status)
    return success_response(data, "Disaster status updated")
