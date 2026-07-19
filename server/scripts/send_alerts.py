#!/usr/bin/env python3
"""Publishes a new region-wide alert. Usage:
python scripts/send_alerts.py "Title" "Message" high "North Region" """
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.mongodb import close_mongo_connection, connect_to_mongo, get_database  # noqa: E402
from utils.helpers import now_ts  # noqa: E402


async def main(title: str, message: str, severity: str, region: str | None) -> None:
    await connect_to_mongo()
    db = get_database()
    await db["alerts"].insert_one({
        "title": title, "message": message, "severity": severity, "region": region,
        "source": "script", "active": True, "created_at": now_ts(),
    })
    print("Alert published.")
    await close_mongo_connection()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('Usage: python scripts/send_alerts.py "Title" "Message" <severity> [region]')
        sys.exit(1)
    region_arg = sys.argv[4] if len(sys.argv) > 4 else None
    asyncio.run(main(sys.argv[1], sys.argv[2], sys.argv[3], region_arg))
