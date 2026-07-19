"""Routes for shelters."""
from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from controllers import shelter_controller
from database.connection import get_db
from middleware.auth import require_roles
from schemas.shelter_schema import ShelterCreateRequest
from utils.response import success_response

router = APIRouter(prefix="/shelters", tags=["Shelters"])


@router.post("", response_model=None)
async def create_shelter(
    payload: ShelterCreateRequest,
    _admin=Depends(require_roles("admin")),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    data = await shelter_controller.create_shelter(db, payload)
    return success_response(data, "Shelter created", 201)


@router.get("", response_model=None)
async def list_shelters(db: AsyncIOMotorDatabase = Depends(get_db)):
    data = await shelter_controller.list_shelters(db)
    return success_response(data, "Shelters fetched")


@router.get("/nearby", response_model=None)
async def nearby_shelters(
    lat: float = Query(...), lng: float = Query(...), radius_km: float = Query(15),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    data = await shelter_controller.find_nearby_shelters(db, lat, lng, radius_km)
    return success_response(data, "Nearby shelters fetched")


@router.patch("/{shelter_id}/occupancy", response_model=None)
async def update_occupancy(
    shelter_id: str, occupancy: int,
    _admin=Depends(require_roles("admin")),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    data = await shelter_controller.update_shelter_occupancy(db, shelter_id, occupancy)
    return success_response(data, "Shelter occupancy updated")
