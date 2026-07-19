"""Exports a single collection to a JSON file. Usage: python export_json.py <collection> <out.json>"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from bson import json_util  # noqa: E402
from database.mongodb import close_mongo_connection, connect_to_mongo, get_database  # noqa: E402


async def main(collection: str, out_path: str) -> None:
    await connect_to_mongo()
    db = get_database()
    docs = [doc async for doc in db[collection].find({})]
    Path(out_path).write_text(json_util.dumps(docs, indent=2))
    print(f"Exported {len(docs)} documents from '{collection}' to {out_path}")
    await close_mongo_connection()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python export_json.py <collection> <out.json>")
        sys.exit(1)
    asyncio.run(main(sys.argv[1], sys.argv[2]))
