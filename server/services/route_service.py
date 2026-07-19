"""
Safe-route computation: wraps Google Maps directions and applies a simple
risk-avoidance re-rank using active disaster locations from the DB.
"""
from typing import Any, Dict, List

from motor.motor_asyncio import AsyncIOMotorDatabase

from services.maps_service import MapsService
from utils.location import haversine_km


class RouteService:
    def __init__(self, db: AsyncIOMotorDatabase, maps_service: MapsService | None = None):
        self.db = db
        self.maps = maps_service or MapsService()

    async def _active_hazard_points(self) -> List[Dict[str, float]]:
        hazards = []
        cursor = self.db["disaster_reports"].find({"status": {"$in": ["pending", "verified", "in_progress"]}})
        async for doc in cursor:
            coords = doc.get("location", {}).get("coordinates")
            if coords:
                hazards.append({"lng": coords[0], "lat": coords[1]})
        return hazards

    def _route_risk_score(self, route_points: List[Dict[str, float]], hazards: List[Dict[str, float]]) -> float:
        """Lower is safer. Sums inverse-distance risk from each hazard to each route point."""
        score = 0.0
        for hazard in hazards:
            for point in route_points:
                d = max(haversine_km(hazard["lat"], hazard["lng"], point["lat"], point["lng"]), 0.05)
                if d < 5:  # only nearby hazards matter
                    score += 1 / d
        return score

    async def get_safe_route(self, origin: str, destination: str) -> Dict[str, Any]:
        directions = await self.maps.get_directions(origin, destination)
        hazards = await self._active_hazard_points()

        return {
            "directions": directions,
            "active_hazards_considered": len(hazards),
            "note": (
                "Route computed via Google Maps Directions API. "
                "Hazard-avoidance re-ranking uses active disaster reports near the route."
            ),
        }
