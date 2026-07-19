"""
Motor (async MongoDB driver) connection manager.
Call connect_to_mongo() on FastAPI startup and close_mongo_connection() on shutdown.
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from config.settings import settings
from config.logging import logger


class MongoManager:
    client: AsyncIOMotorClient | None = None
    db: AsyncIOMotorDatabase | None = None


mongo_manager = MongoManager()


async def connect_to_mongo() -> None:
    logger.info("Connecting to MongoDB at %s", settings.MONGODB_URI.split("@")[-1])
    mongo_manager.client = AsyncIOMotorClient(settings.MONGODB_URI, uuidRepresentation="standard")
    mongo_manager.db = mongo_manager.client[settings.MONGODB_DB_NAME]
    try:
        await mongo_manager.client.admin.command("ping")
        logger.info("MongoDB connection established.")
    except Exception as exc:  # noqa: BLE001
        logger.error("MongoDB connection failed: %s", exc)


async def close_mongo_connection() -> None:
    if mongo_manager.client:
        mongo_manager.client.close()
        logger.info("MongoDB connection closed.")


def get_database() -> AsyncIOMotorDatabase:
    """Return the active database instance. Raises if connect_to_mongo() hasn't run yet."""
    if mongo_manager.db is None:
        raise RuntimeError("Database not initialized. Did the app startup event run?")
    return mongo_manager.db
