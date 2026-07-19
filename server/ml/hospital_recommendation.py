"""Ranks candidate hospitals for a casualty by distance, bed availability, and speciality match."""
from typing import Dict, List, Optional

from utils.location import haversine_km


def recommend_hospitals(
    patient_lat: float, patient_lng: float, hospitals: List[Dict], required_speciality: Optional[str] = None, top_n: int = 3
) -> List[Dict]:
    scored = []

    for hospital in hospitals:
        coords = hospital["location"]["coordinates"]
        distance = haversine_km(patient_lat, patient_lng, coords[1], coords[0])
        beds = hospital.get("beds_available", 0)

        if beds <= 0:
            continue

        speciality_match = 1 if required_speciality and required_speciality in hospital.get("specialities", []) else 0
        score = (1 / (distance + 0.1)) * 10 + (beds / 20) + (speciality_match * 5)

        scored.append({**hospital, "distance_km": round(distance, 2), "score": round(score, 2)})

    scored.sort(key=lambda h: h["score"], reverse=True)
    return scored[:top_n]
