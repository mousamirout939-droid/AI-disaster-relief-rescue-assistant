#!/usr/bin/env python3
"""Generates a plain-text summary report of current disaster-relief activity."""
import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.mongodb import close_mongo_connection, connect_to_mongo, get_database  # noqa: E402

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "reports"


async def main() -> None:
    await connect_to_mongo()
    db = get_database()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total_reports = await db["disaster_reports"].count_documents({})
    pending = await db["disaster_reports"].count_documents({"status": "pending"})
    resolved = await db["disaster_reports"].count_documents({"status": "resolved"})
    shelters = await db["shelters"].count_documents({})
    teams_available = await db["rescue_teams"].count_documents({"status": "available"})

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    content = (
        f"Disaster Relief Activity Report\nGenerated: {stamp}\n\n"
        f"Total reports: {total_reports}\nPending: {pending}\nResolved: {resolved}\n"
        f"Shelters registered: {shelters}\nRescue teams available: {teams_available}\n"
    )

    out_file = OUTPUT_DIR / f"report_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.txt"
    out_file.write_text(content)
    print(content)
    print(f"Saved to {out_file}")

    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())
