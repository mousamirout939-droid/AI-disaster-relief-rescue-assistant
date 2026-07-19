"""
Very lightweight disaster-likelihood forecast: looks at recent report
frequency in a region to flag a rising trend. Falls back to a trained
regressor (ml/models/forecast_model.pkl) if present.
"""
from typing import Dict, List

from ml.config import FORECAST_MODEL_PATH
from ml.utils import load_model


class DisasterForecaster:
    def __init__(self):
        self.model = load_model(FORECAST_MODEL_PATH)

    def forecast_trend(self, recent_report_counts_by_day: List[int]) -> Dict:
        if self.model is not None:
            import numpy as np
            x = np.array([recent_report_counts_by_day])
            prediction = float(self.model.predict(x)[0])
            return {"predicted_next_day_reports": round(prediction, 1), "source": "trained_model"}

        return self._heuristic(recent_report_counts_by_day)

    def _heuristic(self, counts: List[int]) -> Dict:
        if len(counts) < 2:
            return {"predicted_next_day_reports": counts[-1] if counts else 0, "source": "heuristic"}

        # simple linear trend over the last N days
        n = len(counts)
        avg_delta = (counts[-1] - counts[0]) / (n - 1)
        prediction = max(counts[-1] + avg_delta, 0)
        return {"predicted_next_day_reports": round(prediction, 1), "source": "heuristic"}
