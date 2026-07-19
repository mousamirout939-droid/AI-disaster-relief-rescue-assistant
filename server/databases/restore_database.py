"""Re-export of server/scripts/restore_database.py."""
import sys
from scripts.restore_database import main  # noqa: F401

if __name__ == "__main__":
    import asyncio
    if len(sys.argv) != 2:
        print("Usage: python databases/restore_database.py <backup_file.json>")
        sys.exit(1)
    asyncio.run(main(sys.argv[1]))
