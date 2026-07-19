"""
Creates MongoDB indexes for all collections. Run once at startup (idempotent).
"""
from motor.motor_asyncio import AsyncIOMotorDatabase

from config.logging import logger


async def create_indexes(db: AsyncIOMotorDatabase) -> None:
    await db["users"].create_index("email", unique=True)
    await db["users"].create_index("role")

    await db["admins"].create_index("email", unique=True)

    await db["disaster_reports"].create_index([("location", "2dsphere")])
    await db["disaster_reports"].create_index("status")
    await db["disaster_reports"].create_index("created_at")

    await db["shelters"].create_index([("location", "2dsphere")])
    await db["hospitals"].create_index([("location", "2dsphere")])
    await db["rescue_teams"].create_index([("location", "2dsphere")])
    await db["rescue_teams"].create_index("status")

    await db["volunteers"].create_index("email", unique=True)
    await db["emergency_contacts"].create_index("user_id")
    await db["notifications"].create_index("user_id")
    await db["notifications"].create_index("created_at")

    logger.info("MongoDB indexes ensured.")
