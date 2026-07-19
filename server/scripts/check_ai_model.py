#!/usr/bin/env python3
"""Verifies the YOLO weights file exists and loads without error."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config.settings import settings  # noqa: E402
from services.yolo_service import YoloService  # noqa: E402


def main() -> None:
    weights_path = Path(settings.YOLO_WEIGHTS_PATH)
    if not weights_path.exists():
        print(f"WARNING: weights not found at {weights_path}. The API will use the mock detector.")
    else:
        print(f"Weights found at {weights_path}.")

    service = YoloService()
    status = "real YOLO model" if service.model is not None else "mock detector (no trained weights loaded)"
    print(f"AI service is currently using: {status}")


if __name__ == "__main__":
    main()
