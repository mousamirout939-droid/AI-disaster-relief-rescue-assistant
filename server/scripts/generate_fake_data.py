#!/usr/bin/env python3
"""Generates randomized demo data (reports, shelters, hospitals, rescue teams) for load-testing the UI."""
import asyncio
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.mongodb import close_mongo_connection, connect_to_mongo, get_database  # noqa: E402
from utils.constants import DisasterType  # noqa: E402
from utils.helpers import now_ts  # noqa: E402

# Roughly the Bengaluru metro area bounding box, for realistic-looking demo coordinates.
LAT_RANGE = (12.85, 13.05)
LNG_RANGE = (77.45, 77.75)


def _rand_point():
    lat = round(random.uniform(*LAT_RANGE), 5)
    lng = round(random.uniform(*LNG_RANGE), 5)
    return lat, lng


async def main(n: int = 25) -> None:
    await connect_to_mongo()
    db = get_database()

    for i in range(n):
        lat, lng = _rand_point()
        await db["disaster_reports"].insert_one({
            "user_id": "seed-script",
            "disaster_type": random.choice(list(DisasterType)).value,
            "description": f"Auto-generated demo report #{i}",
            "location": {"type": "Point", "coordinates": [lng, lat]},
            "address": None,
            "image_url": None,
            "ai_detections": [],
            "ai_severity": random.choice(["low", "moderate", "high", "critical"]),
            "ai_confidence": round(random.uniform(0.3, 0.95), 2),
            "status": random.choice(["pending", "verified", "in_progress", "resolved"]),
            "verified_by_admin": False,
            "created_at": now_ts(),
        })

    print(f"Inserted {n} fake disaster reports.")
    await close_mongo_connection()


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    asyncio.run(main(count))
