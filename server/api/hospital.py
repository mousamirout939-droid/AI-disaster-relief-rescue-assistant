"""Routes for hospitals."""
from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from controllers import hospital_controller
from database.connection import get_db
from middleware.auth import require_roles
from schemas.hospital_schema import HospitalCreateRequest
from utils.response import success_response

router = APIRouter(prefix="/hospitals", tags=["Hospitals"])


@router.post("", response_model=None)
async def create_hospital(
    payload: HospitalCreateRequest,
    _admin=Depends(require_roles("admin")),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    data = await hospital_controller.create_hospital(db, payload)
    return success_response(data, "Hospital created", 201)


@router.get("", response_model=None)
async def list_hospitals(db: AsyncIOMotorDatabase = Depends(get_db)):
    data = await hospital_controller.list_hospitals(db)
    return success_response(data, "Hospitals fetched")


@router.get("/nearby", response_model=None)
async def nearby_hospitals(
    lat: float = Query(...), lng: float = Query(...), radius_km: float = Query(15),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    data = await hospital_controller.find_nearby_hospitals(db, lat, lng, radius_km)
    return success_response(data, "Nearby hospitals fetched")
