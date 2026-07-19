"""
Trains a RandomForestClassifier for severity prediction on a labeled CSV
with columns: rainfall_mm, wind_speed_kmh, affected_population_estimate,
reported_count, severity.

If no CSV is supplied, generates a small synthetic dataset so the training
pipeline is demonstrably runnable end-to-end without external data.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from ml.config import RANDOM_STATE, SEVERITY_MODEL_PATH  # noqa: E402
from ml.severity_prediction import FEATURE_ORDER  # noqa: E402
from ml.utils import save_model  # noqa: E402


def _synthetic_dataset(n: int = 400) -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_STATE)
    rainfall = rng.uniform(0, 300, n)
    wind = rng.uniform(0, 150, n)
    population = rng.uniform(0, 10000, n)
    reports = rng.integers(1, 50, n)

    score = rainfall / 100 + wind / 80 + population / 5000 + reports / 20
    severity = np.select(
        [score >= 2.5, score >= 1.5, score >= 0.7],
        ["critical", "high", "moderate"],
        default="low",
    )
    return pd.DataFrame({
        "rainfall_mm": rainfall, "wind_speed_kmh": wind,
        "affected_population_estimate": population, "reported_count": reports,
        "severity": severity,
    })


def train(csv_path: str | None = None) -> dict:
    df = pd.read_csv(csv_path) if csv_path else _synthetic_dataset()

    X = df[FEATURE_ORDER]
    y = df["severity"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)

    model = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    save_model(model, SEVERITY_MODEL_PATH)
    print(f"Severity model trained. Test accuracy: {accuracy:.3f}. Saved to {SEVERITY_MODEL_PATH}")
    return {"accuracy": accuracy}


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    train(path)
