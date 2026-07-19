"""Routes for rescue teams."""
from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from controllers import rescue_controller
from database.connection import get_db
from middleware.auth import require_roles
from schemas.rescue_schema import DispatchRequest, RescueTeamCreateRequest
from utils.response import success_response

router = APIRouter(prefix="/rescue-teams", tags=["Rescue Teams"])


@router.post("", response_model=None)
async def create_team(
    payload: RescueTeamCreateRequest,
    _admin=Depends(require_roles("admin")),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    data = await rescue_controller.create_rescue_team(db, payload)
    return success_response(data, "Rescue team created", 201)


@router.get("", response_model=None)
async def list_teams(db: AsyncIOMotorDatabase = Depends(get_db)):
    data = await rescue_controller.list_rescue_teams(db)
    return success_response(data, "Rescue teams fetched")


@router.get("/nearby", response_model=None)
async def nearby_teams(
    lat: float = Query(...), lng: float = Query(...), radius_km: float = Query(25),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    data = await rescue_controller.find_nearby_rescue_teams(db, lat, lng, radius_km)
    return success_response(data, "Nearby rescue teams fetched")


@router.post("/{team_id}/dispatch", response_model=None)
async def dispatch(
    team_id: str, payload: DispatchRequest,
    _admin=Depends(require_roles("admin")),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    data = await rescue_controller.dispatch_team(db, team_id, payload.report_id)
    return success_response(data, "Rescue team dispatched")
