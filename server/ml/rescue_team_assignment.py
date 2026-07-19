"""Assigns the best-fit available rescue team to an incoming report using specialization + proximity."""
from typing import Dict, List, Optional

from utils.location import haversine_km

_TYPE_TO_SPECIALIZATION = {
    "flood": "flood", "fire": "fire", "earthquake": "search_rescue",
    "cyclone": "general", "tsunami": "flood", "landslide": "search_rescue",
    "building_damage": "search_rescue", "other": "general",
}


def assign_best_team(report_lat: float, report_lng: float, disaster_type: str, teams: List[Dict]) -> Optional[Dict]:
    wanted_spec = _TYPE_TO_SPECIALIZATION.get(disaster_type, "general")
    candidates = [t for t in teams if t.get("status") == "available"]
    if not candidates:
        return None

    def score(team: Dict) -> float:
        coords = team["location"]["coordinates"]
        distance = haversine_km(report_lat, report_lng, coords[1], coords[0])
        spec_bonus = 5 if team.get("specialization") == wanted_spec else 0
        return spec_bonus - distance  # higher is better: prioritise specialization, then closeness

    candidates.sort(key=score, reverse=True)
    return candidates[0]
