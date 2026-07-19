#!/usr/bin/env python3
"""Exports every collection to a timestamped JSON file under server/backups/."""
import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bson import json_util  # noqa: E402
from database.mongodb import close_mongo_connection, connect_to_mongo, get_database  # noqa: E402
from scripts.check_database import COLLECTIONS  # noqa: E402

BACKUP_DIR = Path(__file__).resolve().parent.parent / "backups"


async def main() -> None:
    await connect_to_mongo()
    db = get_database()
    BACKUP_DIR.mkdir(exist_ok=True)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = BACKUP_DIR / f"backup_{stamp}.json"

    dump = {}
    for name in COLLECTIONS:
        dump[name] = [doc async for doc in db[name].find({})]

    out_path.write_text(json_util.dumps(dump, indent=2))
    print(f"Backup written to {out_path}")
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())
