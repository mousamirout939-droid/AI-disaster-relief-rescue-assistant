"""Sanity-checks stored documents against the Pydantic models — flags anything that no longer validates."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from database.mongodb import close_mongo_connection, connect_to_mongo, get_database  # noqa: E402
from models.hospital import HospitalModel  # noqa: E402
from models.shelter import ShelterModel  # noqa: E402
from models.user import UserModel  # noqa: E402

MODEL_FOR_COLLECTION = {"users": UserModel, "shelters": ShelterModel, "hospitals": HospitalModel}


async def main() -> None:
    await connect_to_mongo()
    db = get_database()
    total_errors = 0

    for collection, model_cls in MODEL_FOR_COLLECTION.items():
        async for doc in db[collection].find({}):
            try:
                model_cls.model_validate(doc)
            except Exception as exc:  # noqa: BLE001
                total_errors += 1
                print(f"[{collection}] invalid document _id={doc.get('_id')}: {exc}")

    print(f"\nValidation complete. {total_errors} invalid document(s) found.")
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())
