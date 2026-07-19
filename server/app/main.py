"""
FastAPI application entrypoint.
Run locally with:  uvicorn app.main:app --reload
or:                 python run.py
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import (
    admin, ai, alerts, auth, disaster, emergency, hospital,
    notification, reports, rescue, routes, shelter, translation,
    users, volunteer, weather,
)
from config.logging import logger
from config.settings import settings
from database.indexes import create_indexes
from database.mongodb import close_mongo_connection, connect_to_mongo, get_database
from middleware.cors import setup_cors
from middleware.exception_handler import register_exception_handlers
from middleware.logger import RequestLoggingMiddleware
from middleware.rate_limiter import RateLimiterMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    try:
        await create_indexes(get_database())
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not create indexes (DB may be unreachable): %s", exc)
    logger.info("%s starting up in '%s' mode.", settings.APP_NAME, settings.ENV)
    yield
    await close_mongo_connection()
    logger.info("%s shut down.", settings.APP_NAME)


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered disaster relief, rescue coordination, and emergency response platform.",
    version="1.0.0",
    lifespan=lifespan,
)

setup_cors(app)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimiterMiddleware)
register_exception_handlers(app)

# --- Static file mounts (uploaded images) ---
from fastapi.staticfiles import StaticFiles  # noqa: E402
import os  # noqa: E402

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount(f"/{settings.UPLOAD_DIR}", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# --- Routers ---
API_PREFIX = settings.API_V1_PREFIX
for router in (
    auth.router, users.router, admin.router, disaster.router, reports.router,
    shelter.router, hospital.router, rescue.router, ai.router, alerts.router,
    notification.router, weather.router, translation.router, routes.router,
    emergency.router, volunteer.router,
):
    app.include_router(router, prefix=API_PREFIX)


@app.get("/", tags=["Health"])
async def root():
    return {"service": settings.APP_NAME, "status": "running", "docs": "/docs"}


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
