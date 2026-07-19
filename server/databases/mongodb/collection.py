"""Small helper for getting a typed collection handle without importing motor everywhere."""
from motor.motor_asyncio import AsyncIOMotorCollection

from database.mongodb import get_database


def get_collection(name: str) -> AsyncIOMotorCollection:
    return get_database()[name]
