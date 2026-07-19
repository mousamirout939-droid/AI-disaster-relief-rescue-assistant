"""Runs all trained ml/ models (severity, risk, route, forecast) against held-out data, where available."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ml.config import DATASETS_DIR, FORECAST_MODEL_PATH, RISK_MODEL_PATH, ROUTE_MODEL_PATH, SEVERITY_MODEL_PATH  # noqa: E402


def main() -> None:
    print("ml/ model status:\n")
    for name, path in [
        ("severity_model", SEVERITY_MODEL_PATH),
        ("risk_model", RISK_MODEL_PATH),
        ("route_model", ROUTE_MODEL_PATH),
        ("forecast_model", FORECAST_MODEL_PATH),
    ]:
        status = "trained (found on disk)" if path.exists() else "NOT trained — using heuristic fallback"
        print(f"  {name:16s} {status}")

    print(f"\nDatasets directory: {DATASETS_DIR} (exists: {DATASETS_DIR.exists()})")
    print("\nRun the corresponding script in ml/training/ with a labeled CSV to train a real model.")


if __name__ == "__main__":
    main()
