#!/usr/bin/env python3
"""Broadcasts a one-off system notification to all users. Usage:
python scripts/send_notifications.py "Title" "Message body" """
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.mongodb import close_mongo_connection, connect_to_mongo, get_database  # noqa: E402
from services.notification_service import NotificationService  # noqa: E402
from utils.constants import NotificationType  # noqa: E402


async def main(title: str, message: str) -> None:
    await connect_to_mongo()
    db = get_database()
    service = NotificationService(db)
    await service.create(user_id=None, title=title, message=message, n_type=NotificationType.SYSTEM)
    print("Notification broadcast created.")
    await close_mongo_connection()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python scripts/send_notifications.py "Title" "Message"')
        sys.exit(1)
    asyncio.run(main(sys.argv[1], sys.argv[2]))
