"""Prints a formatted accuracy report for a trained classifier given a labeled CSV of features + labels."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from ml.evaluation.metrics import classification_metrics  # noqa: E402
from ml.severity_prediction import FEATURE_ORDER, SeverityPredictor  # noqa: E402


def main(csv_path: str) -> None:
    df = pd.read_csv(csv_path)
    predictor = SeverityPredictor()

    y_true = df["severity"].tolist()
    y_pred = [predictor.predict(row[FEATURE_ORDER].to_dict()).value for _, row in df.iterrows()]

    metrics = classification_metrics(y_true, y_pred)
    print("Severity model accuracy report:")
    for k, v in metrics.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ml/evaluation/accuracy_report.py <labeled_data.csv>")
        sys.exit(1)
    main(sys.argv[1])
