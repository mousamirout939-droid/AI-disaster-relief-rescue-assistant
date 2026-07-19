"""
Trains a regressor that predicts an area risk score (0-100) from disaster
density/severity features, as an optional upgrade over the rule-based
formula in ml/risk_assessment.py. Uses synthetic data if no CSV is given.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from ml.config import RANDOM_STATE, RISK_MODEL_PATH  # noqa: E402
from ml.utils import save_model  # noqa: E402

FEATURES = ["disaster_count_nearby", "avg_severity_score", "avg_distance_km", "population_density"]


def _synthetic_dataset(n: int = 400) -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_STATE)
    disaster_count = rng.integers(0, 10, n)
    avg_severity = rng.uniform(1, 4, n)
    avg_distance = rng.uniform(0.1, 20, n)
    density = rng.uniform(0.5, 3, n)

    risk = np.clip((disaster_count * avg_severity * 10 / avg_distance) * density, 0, 100)
    return pd.DataFrame({
        "disaster_count_nearby": disaster_count, "avg_severity_score": avg_severity,
        "avg_distance_km": avg_distance, "population_density": density, "risk_score": risk,
    })


def train(csv_path: str | None = None) -> dict:
    df = pd.read_csv(csv_path) if csv_path else _synthetic_dataset()
    X, y = df[FEATURES], df["risk_score"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)

    model = RandomForestRegressor(n_estimators=200, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)

    r2 = model.score(X_test, y_test)
    save_model(model, RISK_MODEL_PATH)
    print(f"Risk model trained. Test R^2: {r2:.3f}. Saved to {RISK_MODEL_PATH}")
    return {"r2": r2}


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    train(path)
