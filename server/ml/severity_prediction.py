"""
Predicts disaster severity from structured features (not the image-based
severity in services/ai_service.py — this is for text/sensor-driven reports,
e.g. rainfall_mm, wind_speed_kmh, affected_population_estimate).

Falls back to a rule-based score if no trained model (ml/models/severity_model.pkl)
is present. Train one with ml/training/train_severity.py.
"""
from typing import Dict

import numpy as np

from ml.config import SEVERITY_MODEL_PATH
from ml.utils import load_model
from utils.constants import SeverityLevel

FEATURE_ORDER = ["rainfall_mm", "wind_speed_kmh", "affected_population_estimate", "reported_count"]


class SeverityPredictor:
    def __init__(self):
        self.model = load_model(SEVERITY_MODEL_PATH)

    def predict(self, features: Dict[str, float]) -> SeverityLevel:
        if self.model is not None:
            x = np.array([[features.get(f, 0.0) for f in FEATURE_ORDER]])
            label = self.model.predict(x)[0]
            return SeverityLevel(label)
        return self._heuristic(features)

    def _heuristic(self, features: Dict[str, float]) -> SeverityLevel:
        rainfall = features.get("rainfall_mm", 0)
        wind = features.get("wind_speed_kmh", 0)
        population = features.get("affected_population_estimate", 0)
        reports = features.get("reported_count", 1)

        score = (rainfall / 100) + (wind / 80) + (population / 5000) + (reports / 20)

        if score >= 2.5:
            return SeverityLevel.CRITICAL
        if score >= 1.5:
            return SeverityLevel.HIGH
        if score >= 0.7:
            return SeverityLevel.MODERATE
        return SeverityLevel.LOW
