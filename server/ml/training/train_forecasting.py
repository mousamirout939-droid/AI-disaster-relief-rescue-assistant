"""Trains a next-day report-count forecaster (linear regression over a sliding window of daily counts)."""
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LinearRegression

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from ml.config import FORECAST_MODEL_PATH  # noqa: E402
from ml.utils import save_model  # noqa: E402

WINDOW = 7


def _synthetic_series(n: int = 200) -> np.ndarray:
    rng = np.random.default_rng(42)
    trend = np.linspace(2, 15, n)
    noise = rng.normal(0, 1.5, n)
    return np.clip(trend + noise, 0, None)


def train() -> dict:
    series = _synthetic_series()
    X, y = [], []
    for i in range(len(series) - WINDOW):
        X.append(series[i:i + WINDOW])
        y.append(series[i + WINDOW])

    model = LinearRegression()
    model.fit(X, y)

    save_model(model, FORECAST_MODEL_PATH)
    print(f"Forecast model trained on synthetic data. Saved to {FORECAST_MODEL_PATH}")
    return {"coefficients": model.coef_.tolist()}


if __name__ == "__main__":
    train()
