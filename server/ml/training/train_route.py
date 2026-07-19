"""Trains a travel-time regressor from historical route_dataset.csv-style records, as an
optional data-driven upgrade over ml/route_prediction.py's fixed multipliers."""
import sys
from pathlib import Path

import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from ml.config import RANDOM_STATE, ROUTE_MODEL_PATH  # noqa: E402
from ml.utils import save_model  # noqa: E402

FEATURES = ["distance_km", "hour_of_day", "is_raining", "traffic_density"]


def train(csv_path: str) -> dict:
    df = pd.read_csv(csv_path)
    X, y = df[FEATURES], df["travel_time_minutes"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)

    model = GradientBoostingRegressor(random_state=RANDOM_STATE)
    model.fit(X_train, y_train)

    r2 = model.score(X_test, y_test)
    save_model(model, ROUTE_MODEL_PATH)
    print(f"Route model trained. Test R^2: {r2:.3f}. Saved to {ROUTE_MODEL_PATH}")
    return {"r2": r2}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ml/training/train_route.py <route_dataset.csv>")
        sys.exit(1)
    train(sys.argv[1])
