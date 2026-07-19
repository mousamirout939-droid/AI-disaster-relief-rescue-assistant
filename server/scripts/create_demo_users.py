#!/usr/bin/env python3
"""Creates a handful of demo accounts (user, volunteer, rescue team, admin) for grading/demo purposes."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.security import hash_password  # noqa: E402
from database.mongodb import close_mongo_connection, connect_to_mongo, get_database  # noqa: E402
from utils.helpers import now_ts  # noqa: E402

DEMO_ACCOUNTS = [
    {"name": "Demo User", "email": "user@demo.com", "password": "Password123", "role": "user"},
    {"name": "Demo Volunteer", "email": "volunteer@demo.com", "password": "Password123", "role": "volunteer"},
    {"name": "Demo Rescue", "email": "rescue@demo.com", "password": "Password123", "role": "rescue_team"},
]


async def main() -> None:
    await connect_to_mongo()
    db = get_database()

    for acc in DEMO_ACCOUNTS:
        if await db["users"].find_one({"email": acc["email"]}):
            print(f"Skipping existing {acc['email']}")
            continue
        await db["users"].insert_one({
            "name": acc["name"], "email": acc["email"], "password": hash_password(acc["password"]),
            "role": acc["role"], "is_active": True, "is_verified": True, "created_at": now_ts(),
        })
        print(f"Created {acc['role']}: {acc['email']} / {acc['password']}")

    if not await db["admins"].find_one({"email": "admin@demo.com"}):
        await db["admins"].insert_one({
            "name": "Demo Admin", "email": "admin@demo.com", "password": hash_password("Admin123!"),
            "role": "admin", "is_active": True, "created_at": now_ts(),
        })
        print("Created admin: admin@demo.com / Admin123!")

    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())
