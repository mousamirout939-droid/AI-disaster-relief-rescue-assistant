"""OpenWeatherMap integration for weather alerts near a location."""
from typing import Any, Dict

import httpx

from config.settings import settings
from config.logging import logger

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherService:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.OPENWEATHER_API_KEY

    async def get_current_weather(self, lat: float, lng: float) -> Dict[str, Any]:
        if not self.api_key:
            return {"available": False, "message": "OPENWEATHER_API_KEY not configured."}

        params = {"lat": lat, "lon": lng, "appid": self.api_key, "units": "metric"}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(BASE_URL, params=params)
                resp.raise_for_status()
                data = resp.json()
        except Exception as exc:  # noqa: BLE001
            logger.error("Weather API call failed: %s", exc)
            return {"available": False, "message": "Weather service unavailable."}

        return {
            "available": True,
            "temperature_c": data.get("main", {}).get("temp"),
            "condition": data.get("weather", [{}])[0].get("main"),
            "description": data.get("weather", [{}])[0].get("description"),
            "wind_speed_mps": data.get("wind", {}).get("speed"),
            "humidity": data.get("main", {}).get("humidity"),
            "raw": data,
        }
