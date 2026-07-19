"""
Lightweight migration runner. Migrations are plain async functions named
`migration_<NNN>_<description>` inside databases/scripts/ (none are required
for the current schema — this exists as the hook point for future changes).
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.mongodb import close_mongo_connection, connect_to_mongo, get_database  # noqa: E402


async def main() -> None:
    await connect_to_mongo()
    db = get_database()
    await db["_migrations"].create_index("name", unique=True)
    print("No pending migrations. (Add migration functions to databases/migrate.py as the schema evolves.)")
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())
