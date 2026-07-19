"""Small generic helpers used across controllers/services."""
import random
import string
from datetime import datetime, timezone
from typing import Any, Dict


def now_ts() -> float:
    return datetime.now(timezone.utc).timestamp()


def generate_otp(length: int = 6) -> str:
    return "".join(random.choices(string.digits, k=length))


def serialize_mongo_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Converts a raw Mongo document (with ObjectId `_id`) into a JSON-safe dict."""
    if not doc:
        return doc
    result = dict(doc)
    if "_id" in result:
        result["id"] = str(result.pop("_id"))
    return result


def paginate(query_params: Dict[str, Any]) -> tuple[int, int]:
    page = max(int(query_params.get("page", 1)), 1)
    limit = min(max(int(query_params.get("limit", 20)), 1), 100)
    skip = (page - 1) * limit
    return skip, limit
