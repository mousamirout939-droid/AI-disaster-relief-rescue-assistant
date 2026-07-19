"""Provides singleton instances of the AI services (YOLO + Gemini) to routes via DI."""
from functools import lru_cache

from services.yolo_service import YoloService
from services.gemini_service import GeminiService


@lru_cache
def get_yolo_service() -> YoloService:
    return YoloService()


@lru_cache
def get_gemini_service() -> GeminiService:
    return GeminiService()
