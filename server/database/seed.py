"""
Seeds the database with demo data for local development / grading demos.
Run with: python -m database.seed   (or via scripts/seed_database.py)
"""
import asyncio
from datetime import datetime, timezone

from config.security import hash_password
from database.mongodb import connect_to_mongo, close_mongo_connection, get_database


async def seed() -> None:
    await connect_to_mongo()
    db = get_database()

    if await db["users"].count_documents({}) == 0:
        await db["users"].insert_one({
            "name": "Demo User",
            "email": "user@demo.com",
            "password": hash_password("Password123!"),
            "role": "user",
            "phone": "+911234567890",
            "created_at": datetime.now(timezone.utc),
        })

    if await db["admins"].count_documents({}) == 0:
        await db["admins"].insert_one({
            "name": "Admin",
            "email": "admin@demo.com",
            "password": hash_password("Admin123!"),
            "role": "admin",
            "created_at": datetime.now(timezone.utc),
        })

    if await db["shelters"].count_documents({}) == 0:
        await db["shelters"].insert_many([
            {
                "name": "Central Community Shelter",
                "capacity": 200,
                "occupancy": 45,
                "location": {"type": "Point", "coordinates": [77.5946, 12.9716]},
                "address": "MG Road, Bengaluru",
                "contact_number": "+911111111111",
                "resources": ["food", "water", "medical"],
                "status": "open",
            },
        ])

    if await db["hospitals"].count_documents({}) == 0:
        await db["hospitals"].insert_many([
            {
                "name": "City General Hospital",
                "location": {"type": "Point", "coordinates": [77.6033, 12.9772]},
                "address": "Brigade Road, Bengaluru",
                "contact_number": "+912222222222",
                "beds_available": 30,
                "specialities": ["trauma", "general"],
            },
        ])

    print("Seed complete.")
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed())
