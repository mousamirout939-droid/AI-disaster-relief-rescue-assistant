#!/usr/bin/env python3
"""
Scheduled maintenance entrypoint — intended to be triggered by an external
scheduler (cron, Render Cron Job, GitHub Actions schedule). Chains together
the cleanup and backup scripts.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.backup_database import main as backup_main  # noqa: E402
from scripts.clean_database import main as clean_main  # noqa: E402


async def run_all() -> None:
    print("Running scheduled cleanup...")
    await clean_main()
    print("Running scheduled backup...")
    await backup_main()
    print("Cron job complete.")


if __name__ == "__main__":
    asyncio.run(run_all())
