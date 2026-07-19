"""
FastAPI dependency wrapper around the Mongo database instance.
Import `get_db` in routers: `db = Depends(get_db)`.
"""
from motor.motor_asyncio import AsyncIOMotorDatabase

from database.mongodb import get_database


async def get_db() -> AsyncIOMotorDatabase:
    return get_database()
