"""Computes a 0-100 area risk score by combining active-disaster density, severity, and population proximity."""
from typing import List

from utils.constants import SEVERITY_ORDER


def compute_area_risk_score(nearby_disasters: List[dict], population_density: float = 1.0) -> float:
    """
    nearby_disasters: list of {"severity": <SeverityLevel value>, "distance_km": float}
    Closer + more severe + more numerous disasters increase the score.
    """
    if not nearby_disasters:
        return 0.0

    total = 0.0
    for d in nearby_disasters:
        severity_weight = SEVERITY_ORDER.get(d["severity"], 1) if not isinstance(d["severity"], str) else {
            "low": 1, "moderate": 2, "high": 3, "critical": 4
        }.get(d["severity"], 1)
        distance = max(d.get("distance_km", 1.0), 0.1)
        total += (severity_weight * 10) / distance

    score = min(total * population_density, 100.0)
    return round(score, 1)


def risk_category(score: float) -> str:
    if score >= 70:
        return "critical"
    if score >= 40:
        return "high"
    if score >= 15:
        return "moderate"
    return "low"
