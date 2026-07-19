"""Business logic wrapper around RouteService for the safe-route endpoint."""
from typing import Any, Dict

from motor.motor_asyncio import AsyncIOMotorDatabase

from services.route_service import RouteService


async def compute_safe_route(db: AsyncIOMotorDatabase, origin: str, destination: str) -> Dict[str, Any]:
    service = RouteService(db)
    return await service.get_safe_route(origin, destination)
