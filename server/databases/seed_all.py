"""Seeds core demo data (database/seed.py) plus the JSON fixtures in databases/seeds/."""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.mongodb import close_mongo_connection, connect_to_mongo, get_database  # noqa: E402
from database.seed import seed  # noqa: E402

SEEDS_DIR = Path(__file__).resolve().parent / "seeds"
COLLECTION_FOR_FILE = {
    "users.json": "users", "admins.json": "admins", "shelters.json": "shelters",
    "hospitals.json": "hospitals", "rescue_teams.json": "rescue_teams",
    "volunteers.json": "volunteers", "alerts.json": "alerts",
    "disaster_reports.json": "disaster_reports", "emergency_contacts.json": "emergency_contacts",
    "medical_camps.json": "medical_camps", "food_centers.json": "food_centers",
    "relief_materials.json": "relief_materials",
}


async def main() -> None:
    await seed()  # base demo user/admin/shelter/hospital from database/seed.py
    await connect_to_mongo()
    db = get_database()

    for filename, collection in COLLECTION_FOR_FILE.items():
        path = SEEDS_DIR / filename
        if not path.exists():
            continue
        docs = json.loads(path.read_text())
        if not docs:
            continue
        if await db[collection].count_documents({}) == 0:
            await db[collection].insert_many(docs)
            print(f"Seeded {len(docs)} into {collection}")

    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())
