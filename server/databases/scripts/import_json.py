"""Imports a JSON array of documents into a collection. Usage: python import_json.py <collection> <file.json>"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from bson import json_util  # noqa: E402
from database.mongodb import close_mongo_connection, connect_to_mongo, get_database  # noqa: E402


async def main(collection: str, in_path: str) -> None:
    docs = json_util.loads(Path(in_path).read_text())
    if not docs:
        print("Nothing to import.")
        return

    await connect_to_mongo()
    db = get_database()
    result = await db[collection].insert_many(docs)
    print(f"Imported {len(result.inserted_ids)} documents into '{collection}'")
    await close_mongo_connection()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python import_json.py <collection> <file.json>")
        sys.exit(1)
    asyncio.run(main(sys.argv[1], sys.argv[2]))
