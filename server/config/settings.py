"""
Application-wide configuration loaded from environment variables.
Uses pydantic-settings so values are validated once at startup.
"""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "AI Disaster Relief & Rescue Assistant"
    ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # --- Security / JWT ---
    JWT_SECRET_KEY: str = "change-this-secret-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24        # 1 day
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7    # 7 days

    # --- MongoDB ---
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "disaster_relief_db"

    # --- CORS ---
    # Allowing local development and wildcard/explicit Vercel URLs to prevent CORS blockages
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173", 
        "http://localhost:3000",
        "https://ai-disaster-relief-rescue-assistant.vercel.app",
        "*"
    ]

    # --- Third-party APIs ---
    GEMINI_API_KEY: str = ""
    GOOGLE_MAPS_API_KEY: str = ""
    OPENWEATHER_API_KEY: str = ""

    # --- Email (SMTP) ---
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "no-reply@disaster-relief.app"

    # --- File uploads ---
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_IMAGE_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".webp"]

    # --- AI / YOLO ---
    YOLO_WEIGHTS_PATH: str = "weights/best.pt"
    YOLO_CONFIDENCE_THRESHOLD: float = 0.35

    # --- Rate limiting ---
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> "Settings":
    """Cached settings instance so we parse the environment only once."""
    return Settings()


settings = get_settings()