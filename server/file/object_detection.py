"""Re-export of the real YOLO detection call."""
from services.yolo_service import YoloService


def detect_objects(image_path: str, weights_path: str | None = None) -> list[dict]:
    return YoloService(weights_path).detect(image_path)
