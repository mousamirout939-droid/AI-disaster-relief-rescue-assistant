"""Re-export of server/scripts/backup_database.py."""
from scripts.backup_database import main  # noqa: F401

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
