"""Basic OpenCV/NumPy preprocessing shared by the YOLO inference pipeline."""
from typing import Tuple

import cv2
import numpy as np


def load_image(path: str) -> np.ndarray:
    image = cv2.imread(path)
    if image is None:
        raise ValueError(f"Could not read image at {path}")
    return image


def resize_image(image: np.ndarray, size: Tuple[int, int] = (640, 640)) -> np.ndarray:
    return cv2.resize(image, size, interpolation=cv2.INTER_AREA)


def normalize_image(image: np.ndarray) -> np.ndarray:
    return (image.astype(np.float32) / 255.0)


def to_grayscale(image: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def draw_detections(image: np.ndarray, detections: list[dict]) -> np.ndarray:
    """Draw YOLO bounding boxes + labels on a copy of the image for the annotated preview."""
    annotated = image.copy()
    for det in detections:
        x1, y1, x2, y2 = det["box"]
        label = f"{det['class_name']} {det['confidence']:.2f}"
        cv2.rectangle(annotated, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
        cv2.putText(annotated, label, (int(x1), max(int(y1) - 10, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    return annotated
