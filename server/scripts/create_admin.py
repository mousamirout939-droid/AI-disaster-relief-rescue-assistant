#!/usr/bin/env python3
"""
CLI helper to create an admin account directly in MongoDB.
Usage: python scripts/create_admin.py --email admin@x.com --password Secret123 --name "Site Admin"
"""
import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.security import hash_password  # noqa: E402
from database.mongodb import close_mongo_connection, connect_to_mongo, get_database  # noqa: E402
from utils.helpers import now_ts  # noqa: E402


async def main(email: str, password: str, name: str) -> None:
    await connect_to_mongo()
    db = get_database()

    existing = await db["admins"].find_one({"email": email})
    if existing:
        print(f"Admin with email {email} already exists.")
    else:
        await db["admins"].insert_one({
            "name": name, "email": email, "password": hash_password(password),
            "role": "admin", "is_active": True, "created_at": now_ts(),
        })
        print(f"Admin account created for {email}.")

    await close_mongo_connection()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--name", default="Admin")
    args = parser.parse_args()
    asyncio.run(main(args.email, args.password, args.name))
