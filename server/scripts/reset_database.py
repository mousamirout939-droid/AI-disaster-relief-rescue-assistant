#!/usr/bin/env python3
"""DANGEROUS: drops every collection. Prompts for confirmation unless --yes is passed."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.mongodb import close_mongo_connection, connect_to_mongo, get_database  # noqa: E402
from scripts.check_database import COLLECTIONS  # noqa: E402


async def main(confirmed: bool) -> None:
    if not confirmed:
        answer = input("This will DROP ALL collections. Type 'yes' to continue: ")
        confirmed = answer.strip().lower() == "yes"
    if not confirmed:
        print("Aborted.")
        return

    await connect_to_mongo()
    db = get_database()
    for name in COLLECTIONS:
        await db[name].drop()
        print(f"Dropped {name}")
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main("--yes" in sys.argv))
