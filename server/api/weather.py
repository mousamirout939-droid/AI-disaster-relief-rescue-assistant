"""Weather alert routes (OpenWeatherMap passthrough)."""
from fastapi import APIRouter, Query

from services.weather_service import WeatherService
from utils.response import success_response

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("/current", response_model=None)
async def current_weather(lat: float = Query(...), lng: float = Query(...)):
    service = WeatherService()
    data = await service.get_current_weather(lat, lng)
    return success_response(data, "Weather fetched")
