"""Aggregates per-detection confidences into a single overall confidence score for a report."""
from typing import List


def aggregate_confidence(detections: List[dict]) -> float:
    if not detections:
        return 0.0
    return round(sum(d["confidence"] for d in detections) / len(detections), 3)


def max_confidence(detections: List[dict]) -> float:
    if not detections:
        return 0.0
    return round(max(d["confidence"] for d in detections), 3)
