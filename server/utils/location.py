"""Geospatial helper functions (Haversine distance, nearby query builder)."""
import math
from typing import Any, Dict


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two lat/lon points, in kilometres."""
    r = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def near_query(lng: float, lat: float, max_distance_km: float = 10) -> Dict[str, Any]:
    """Build a MongoDB $nearSphere geo query for a 2dsphere-indexed `location` field."""
    return {
        "location": {
            "$nearSphere": {
                "$geometry": {"type": "Point", "coordinates": [lng, lat]},
                "$maxDistance": max_distance_km * 1000,
            }
        }
    }
