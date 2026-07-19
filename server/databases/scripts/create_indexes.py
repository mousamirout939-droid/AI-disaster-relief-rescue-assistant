"""CLI: python databases/scripts/create_indexes.py"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from database.indexes import create_indexes  # noqa: E402
from database.mongodb import close_mongo_connection, connect_to_mongo, get_database  # noqa: E402


async def main() -> None:
    await connect_to_mongo()
    await create_indexes(get_database())
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())
