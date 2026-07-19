"""Estimates a congestion multiplier from a traffic_data.csv-style feed (time-of-day + reported density)."""
from datetime import datetime
from typing import Dict


def estimate_congestion_multiplier(hour: int | None = None, reported_density: float = 0.5) -> float:
    """reported_density: 0 (empty roads) to 1 (gridlock)."""
    hour = hour if hour is not None else datetime.now().hour
    peak_hours = {8, 9, 18, 19}
    peak_bonus = 0.4 if hour in peak_hours else 0.0
    return round(1.0 + peak_bonus + reported_density, 2)
