"""
YOLOv8 disaster-detection inference service (Ultralytics).

If the weights file isn't present (e.g. it wasn't downloaded/trained), the
service falls back to a heuristic "mock" detector so the rest of the app
(reporting flow, severity pipeline) keeps working end-to-end in a demo.
"""
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from config.settings import settings
from config.logging import logger
from utils.image_processing import load_image

_DISASTER_CLASSES = [
    "flood", "fire", "earthquake_damage", "cyclone_damage",
    "landslide", "building_collapse", "debris", "flooded_road",
]


class YoloService:
    def __init__(self, weights_path: str | None = None):
        self.weights_path = Path(weights_path or settings.YOLO_WEIGHTS_PATH)
        self.model = None
        self._load_model()

    def _load_model(self) -> None:
        if not self.weights_path.exists():
            logger.warning(
                "YOLO weights not found at %s — using mock detector. "
                "Place a trained .pt file there to enable real inference.",
                self.weights_path,
            )
            return
        try:
            from ultralytics import YOLO  # imported lazily; heavy dependency
            self.model = YOLO(str(self.weights_path))
            logger.info("YOLO model loaded from %s", self.weights_path)
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to load YOLO model (%s). Falling back to mock detector.", exc)
            self.model = None

    def detect(self, image_path: str) -> List[Dict[str, Any]]:
        """Runs inference and returns a list of {class_name, confidence, box}."""
        if self.model is not None:
            return self._real_detect(image_path)
        return self._mock_detect(image_path)

    def _real_detect(self, image_path: str) -> List[Dict[str, Any]]:
        results = self.model.predict(
            source=image_path, conf=settings.YOLO_CONFIDENCE_THRESHOLD, verbose=False
        )
        detections: List[Dict[str, Any]] = []
        for r in results:
            names = r.names
            for box in r.boxes:
                cls_id = int(box.cls[0])
                detections.append({
                    "class_name": names.get(cls_id, str(cls_id)),
                    "confidence": float(box.conf[0]),
                    "box": [float(x) for x in box.xyxy[0].tolist()],
                })
        return detections

    def _mock_detect(self, image_path: str) -> List[Dict[str, Any]]:
        """Deterministic pseudo-detection based on image statistics, used only when no
        trained weights are available. NOT a substitute for the real model."""
        try:
            image = load_image(image_path)
        except ValueError:
            return []

        avg_color = image.mean(axis=(0, 1))  # BGR
        b, g, r = avg_color
        h, w = image.shape[:2]

        # crude colour heuristics just so the pipeline has something to work with
        if r > 140 and r > g + 40 and r > b + 40:
            cls_name, conf = "fire", 0.55
        elif b > 120 and b > r + 20:
            cls_name, conf = "flood", 0.50
        else:
            cls_name, conf = "debris", 0.35

        return [{
            "class_name": cls_name,
            "confidence": conf,
            "box": [w * 0.1, h * 0.1, w * 0.9, h * 0.9],
        }]
