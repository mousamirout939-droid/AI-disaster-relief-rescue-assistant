"""Ranks candidate shelters for a group of evacuees by distance, remaining capacity, and resource match."""
from typing import Dict, List

from utils.location import haversine_km


def recommend_shelters(
    evacuee_lat: float, evacuee_lng: float, shelters: List[Dict], needed_resources: List[str] | None = None, top_n: int = 3
) -> List[Dict]:
    needed = set(needed_resources or [])
    scored = []

    for shelter in shelters:
        coords = shelter["location"]["coordinates"]
        distance = haversine_km(evacuee_lat, evacuee_lng, coords[1], coords[0])
        remaining_capacity = max(shelter.get("capacity", 0) - shelter.get("occupancy", 0), 0)

        if remaining_capacity <= 0 or shelter.get("status") != "open":
            continue

        resource_match = len(needed & set(shelter.get("resources", []))) if needed else 0
        # lower distance is better, higher capacity/resource match is better
        score = (1 / (distance + 0.1)) * 10 + (remaining_capacity / 50) + (resource_match * 2)

        scored.append({**shelter, "distance_km": round(distance, 2), "remaining_capacity": remaining_capacity, "score": round(score, 2)})

    scored.sort(key=lambda s: s["score"], reverse=True)
    return scored[:top_n]
