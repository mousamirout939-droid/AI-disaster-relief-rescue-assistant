"""
High-level emergency workflow: handles SOS triggers by finding the nearest
rescue team + hospital and firing off a notification/alert.
"""
from typing import Any, Dict

from motor.motor_asyncio import AsyncIOMotorDatabase

from services.notification_service import NotificationService
from utils.location import near_query, haversine_km


class EmergencyService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.notifications = NotificationService(db)

    async def trigger_sos(self, user_id: str, lat: float, lng: float) -> Dict[str, Any]:
        nearest_team = await self.db["rescue_teams"].find_one(
            {**near_query(lng, lat, max_distance_km=25), "status": "available"}
        )
        nearest_hospital = await self.db["hospitals"].find_one(near_query(lng, lat, max_distance_km=25))

        await self.notifications.broadcast_sos(user_id, lat, lng)

        response: Dict[str, Any] = {"sos_received": True}

        if nearest_team:
            coords = nearest_team["location"]["coordinates"]
            response["nearest_rescue_team"] = {
                "id": str(nearest_team["_id"]),
                "name": nearest_team["name"],
                "distance_km": round(haversine_km(lat, lng, coords[1], coords[0]), 2),
            }
        if nearest_hospital:
            coords = nearest_hospital["location"]["coordinates"]
            response["nearest_hospital"] = {
                "id": str(nearest_hospital["_id"]),
                "name": nearest_hospital["name"],
                "distance_km": round(haversine_km(lat, lng, coords[1], coords[0]), 2),
            }

        return response
