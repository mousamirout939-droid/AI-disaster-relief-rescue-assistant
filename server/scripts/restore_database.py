#!/usr/bin/env python3
"""Restores collections from a JSON backup produced by backup_database.py.
Usage: python scripts/restore_database.py backups/backup_20260101_000000.json"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bson import json_util  # noqa: E402
from database.mongodb import close_mongo_connection, connect_to_mongo, get_database  # noqa: E402


async def main(backup_file: str) -> None:
    path = Path(backup_file)
    if not path.exists():
        print(f"Backup file not found: {path}")
        return

    data = json_util.loads(path.read_text())
    await connect_to_mongo()
    db = get_database()

    for collection_name, docs in data.items():
        if not docs:
            continue
        await db[collection_name].delete_many({})
        await db[collection_name].insert_many(docs)
        print(f"Restored {len(docs)} documents into {collection_name}")

    await close_mongo_connection()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/restore_database.py <backup_file.json>")
        sys.exit(1)
    asyncio.run(main(sys.argv[1]))
