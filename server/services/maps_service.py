"""Google Maps Directions/Distance Matrix integration for safe-route suggestions."""
from typing import Any, Dict

import httpx

from config.settings import settings
from config.logging import logger

DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json"


class MapsService:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.GOOGLE_MAPS_API_KEY

    async def get_directions(self, origin: str, destination: str, avoid: str | None = None) -> Dict[str, Any]:
        if not self.api_key:
            return {"available": False, "message": "GOOGLE_MAPS_API_KEY not configured."}

        params = {"origin": origin, "destination": destination, "key": self.api_key}
        if avoid:
            params["avoid"] = avoid

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(DIRECTIONS_URL, params=params)
                resp.raise_for_status()
                data = resp.json()
        except Exception as exc:  # noqa: BLE001
            logger.error("Google Maps API call failed: %s", exc)
            return {"available": False, "message": "Maps service unavailable."}

        return {"available": True, "raw": data}
