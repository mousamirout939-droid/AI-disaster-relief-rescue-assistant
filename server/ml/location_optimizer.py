"""
Suggests an optimal new shelter/resource-depot location for a cluster of
disaster reports, using a simple weighted-centroid (geographic mean) — a
lightweight stand-in for a full k-means facility-location model.
"""
from typing import Dict, List, Tuple


def suggest_location(reports: List[Dict]) -> Tuple[float, float]:
    """Returns (lat, lng) centroid of the given reports' locations, weighted by severity."""
    weight_map = {"low": 1, "moderate": 2, "high": 3, "critical": 4}

    total_weight = 0.0
    lat_sum = 0.0
    lng_sum = 0.0

    for report in reports:
        coords = report["location"]["coordinates"]  # [lng, lat]
        weight = weight_map.get(report.get("ai_severity", "low"), 1)
        lat_sum += coords[1] * weight
        lng_sum += coords[0] * weight
        total_weight += weight

    if total_weight == 0:
        return (0.0, 0.0)

    return (round(lat_sum / total_weight, 6), round(lng_sum / total_weight, 6))
