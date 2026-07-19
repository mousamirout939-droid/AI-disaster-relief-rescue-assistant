"""Re-export of server/database/seed.py (see that module for the canonical implementation)."""
from database.seed import seed  # noqa: F401

if __name__ == "__main__":
    import asyncio
    asyncio.run(seed())
