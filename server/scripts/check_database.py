#!/usr/bin/env python3
"""Pings MongoDB and prints collection document counts — useful for a quick health check."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.mongodb import close_mongo_connection, connect_to_mongo, get_database  # noqa: E402

COLLECTIONS = [
    "users", "admins", "disaster_reports", "disasters", "shelters", "hospitals",
    "rescue_teams", "volunteers", "emergency_contacts", "notifications", "alerts",
]


async def main() -> None:
    await connect_to_mongo()
    db = get_database()
    try:
        await db.client.admin.command("ping")
        print("MongoDB connection: OK\n")
    except Exception as exc:  # noqa: BLE001
        print(f"MongoDB connection FAILED: {exc}")
        return

    for name in COLLECTIONS:
        count = await db[name].count_documents({})
        print(f"{name:22s} {count} documents")

    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())
