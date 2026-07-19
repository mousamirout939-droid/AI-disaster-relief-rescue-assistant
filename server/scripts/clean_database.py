#!/usr/bin/env python3
"""Removes stale data: resolved reports older than 90 days, read notifications older than 30 days."""
import asyncio
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.mongodb import close_mongo_connection, connect_to_mongo, get_database  # noqa: E402

DAY = 86400


async def main() -> None:
    await connect_to_mongo()
    db = get_database()
    now = time.time()

    reports_result = await db["disaster_reports"].delete_many(
        {"status": "resolved", "created_at": {"$lt": now - 90 * DAY}}
    )
    notifications_result = await db["notifications"].delete_many(
        {"read": True, "created_at": {"$lt": now - 30 * DAY}}
    )

    print(f"Removed {reports_result.deleted_count} old resolved reports.")
    print(f"Removed {notifications_result.deleted_count} old read notifications.")
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())
