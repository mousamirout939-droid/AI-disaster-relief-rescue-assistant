"""
Predicts estimated travel time for a route segment, adjusting a base
distance/speed estimate for weather and traffic-like conditions. This
complements services/route_service.py's Google-Maps-based routing with a
lightweight, dependency-free estimate for offline / degraded-network use.
"""
from typing import Dict

BASE_SPEED_KMH = 35  # average urban driving speed assumption

_CONDITION_MULTIPLIERS = {
    "clear": 1.0,
    "rain": 1.3,
    "heavy_rain": 1.8,
    "flood_risk": 2.5,
    "night": 1.15,
}


def estimate_travel_time_minutes(distance_km: float, conditions: Dict[str, bool] | None = None) -> float:
    multiplier = 1.0
    for condition, active in (conditions or {}).items():
        if active:
            multiplier *= _CONDITION_MULTIPLIERS.get(condition, 1.0)

    effective_speed = BASE_SPEED_KMH / multiplier
    return round((distance_km / effective_speed) * 60, 1)
