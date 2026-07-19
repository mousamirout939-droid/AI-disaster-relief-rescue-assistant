"""Creates and stores in-app notifications (push-notification-ready payloads)."""
from typing import Any, Dict, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from utils.constants import NotificationType
from utils.helpers import now_ts


class NotificationService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create(
        self,
        user_id: Optional[str],
        title: str,
        message: str,
        n_type: NotificationType = NotificationType.SYSTEM,
        data: Optional[Dict[str, Any]] = None,
    ) -> str:
        doc = {
            "user_id": user_id,
            "title": title,
            "message": message,
            "type": n_type.value,
            "data": data or {},
            "read": False,
            "created_at": now_ts(),
        }
        result = await self.db["notifications"].insert_one(doc)
        return str(result.inserted_id)

    async def broadcast_sos(self, user_id: str, lat: float, lng: float) -> str:
        return await self.create(
            user_id=None,
            title="🚨 SOS Alert",
            message=f"User {user_id} triggered an SOS at ({lat}, {lng}).",
            n_type=NotificationType.SOS,
            data={"user_id": user_id, "lat": lat, "lng": lng},
        )
