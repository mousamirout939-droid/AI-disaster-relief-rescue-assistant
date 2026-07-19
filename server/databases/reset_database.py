"""Re-export of server/scripts/reset_database.py."""
import sys
from scripts.reset_database import main  # noqa: F401

if __name__ == "__main__":
    import asyncio
    asyncio.run(main("--yes" in sys.argv))
