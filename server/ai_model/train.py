"""
Trains the YOLOv8 disaster-detection model on the dataset described by
`datasets/data.yaml`. Requires a populated dataset (train/valid/test image +
label folders in YOLO format) and the `ultralytics` package.

This is real, runnable training code — it just needs an actual labeled
dataset and GPU/CPU time that aren't available in this environment. See
server/datasets/README.md for how to populate the dataset directory.

Usage:
    python ai_model/train.py --epochs 50 --imgsz 640 --batch 16
"""
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_YAML = BASE_DIR / "datasets" / "data.yaml"
WEIGHTS_OUT = BASE_DIR / "weights"


def train(epochs: int, imgsz: int, batch: int, base_model: str = "yolov8n.pt") -> None:
    from ultralytics import YOLO

    if not DATA_YAML.exists():
        raise FileNotFoundError(
            f"{DATA_YAML} not found. Populate server/datasets/ with a YOLO-format "
            f"dataset and data.yaml before training."
        )

    model = YOLO(base_model)
    results = model.train(data=str(DATA_YAML), epochs=epochs, imgsz=imgsz, batch=batch, project=str(BASE_DIR / "outputs"), name="train")

    WEIGHTS_OUT.mkdir(exist_ok=True)
    best_src = Path(results.save_dir) / "weights" / "best.pt"
    if best_src.exists():
        import shutil
        shutil.copy(best_src, WEIGHTS_OUT / "best.pt")
        print(f"Copied best weights to {WEIGHTS_OUT / 'best.pt'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--base-model", default="yolov8n.pt")
    args = parser.parse_args()
    train(args.epochs, args.imgsz, args.batch, args.base_model)
