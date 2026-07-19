"""Safe-route (navigation) endpoint."""
from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from controllers import route_controller
from database.connection import get_db
from utils.response import success_response

router = APIRouter(prefix="/routes", tags=["Safe Route"])


@router.get("/safe", response_model=None)
async def safe_route(
    origin: str = Query(..., description="'lat,lng' or address"),
    destination: str = Query(..., description="'lat,lng' or address"),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    data = await route_controller.compute_safe_route(db, origin, destination)
    return success_response(data, "Safe route computed")
