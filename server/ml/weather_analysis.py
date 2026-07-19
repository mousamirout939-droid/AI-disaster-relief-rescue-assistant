"""Flags weather conditions that meaningfully raise disaster risk (heavy rain, high wind, storm)."""
from typing import Dict


def assess_weather_risk(weather: Dict) -> Dict:
    condition = (weather.get("condition") or "").lower()
    wind = weather.get("wind_speed_mps", 0) or 0
    risk_flags = []

    if "rain" in condition or "storm" in condition:
        risk_flags.append("heavy_precipitation")
    if wind and wind > 15:
        risk_flags.append("high_wind")
    if "thunder" in condition:
        risk_flags.append("lightning_risk")

    return {"risk_flags": risk_flags, "elevated_risk": len(risk_flags) > 0}
