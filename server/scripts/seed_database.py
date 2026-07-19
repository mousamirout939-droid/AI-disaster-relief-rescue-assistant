#!/usr/bin/env python3
"""Thin CLI wrapper around database/seed.py — `python scripts/seed_database.py`."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.seed import seed  # noqa: E402

if __name__ == "__main__":
    asyncio.run(seed())
