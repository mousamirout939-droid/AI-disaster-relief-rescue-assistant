"""Thin wrapper so ai_model.inference exposes the same detect() call as services/yolo_service.py,
for scripts that operate directly on the training pipeline rather than through the API."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.yolo_service import YoloService  # noqa: E402


def run_inference(image_path: str, weights_path: str | None = None) -> list[dict]:
    service = YoloService(weights_path)
    return service.detect(image_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ai_model/inference.py <image_path> [weights_path]")
        sys.exit(1)
    weights = sys.argv[2] if len(sys.argv) > 2 else None
    print(run_inference(sys.argv[1], weights))
