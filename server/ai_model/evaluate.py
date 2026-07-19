"""Evaluates a trained YOLO model against the validation split and prints mAP metrics."""
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_YAML = BASE_DIR / "datasets" / "data.yaml"


def evaluate(weights_path: str) -> dict:
    from ultralytics import YOLO

    model = YOLO(weights_path)
    metrics = model.val(data=str(DATA_YAML))
    summary = {
        "map50": float(metrics.box.map50),
        "map50_95": float(metrics.box.map),
        "precision": float(metrics.box.mp),
        "recall": float(metrics.box.mr),
    }
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", default=str(BASE_DIR / "weights" / "best.pt"))
    args = parser.parse_args()
    print(evaluate(args.weights))
