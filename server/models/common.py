"""
Shared helpers for Mongo-backed Pydantic models: a JSON/BSON-friendly
ObjectId type and a common base model with Mongo-style config.
"""
from datetime import datetime, timezone
from typing import Annotated, Any

from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field


def _validate_object_id(v: Any) -> str:
    if isinstance(v, ObjectId):
        return str(v)
    if isinstance(v, str) and ObjectId.is_valid(v):
        return v
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[str, BeforeValidator(_validate_object_id)]


class MongoBaseModel(BaseModel):
    """Base class for all documents stored in MongoDB."""

    id: PyObjectId | None = Field(default=None, alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class GeoPoint(BaseModel):
    type: str = "Point"
    coordinates: list[float]  # [longitude, latitude]
