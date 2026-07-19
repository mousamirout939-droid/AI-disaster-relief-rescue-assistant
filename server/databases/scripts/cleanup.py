"""Re-export of server/scripts/clean_database.py."""
from scripts.clean_database import main  # noqa: F401

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
