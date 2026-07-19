"""
Orchestrates the AI pipeline for a submitted disaster report:
image -> YOLO detections -> severity prediction -> structured result.
"""
from typing import Any, Dict, List

from services.yolo_service import YoloService
from utils.constants import SeverityLevel

# relative weight of each detected class toward severity
_CLASS_SEVERITY_WEIGHT = {
    "fire": 0.9,
    "flood": 0.7,
    "building_collapse": 1.0,
    "earthquake_damage": 0.85,
    "cyclone_damage": 0.75,
    "landslide": 0.8,
    "flooded_road": 0.5,
    "debris": 0.3,
}


class AIService:
    def __init__(self, yolo_service: YoloService | None = None):
        self.yolo = yolo_service or YoloService()

    def analyze_report_image(self, image_path: str) -> Dict[str, Any]:
        detections = self.yolo.detect(image_path)
        severity, confidence = self._predict_severity(detections)
        return {
            "detections": detections,
            "severity": severity,
            "confidence": confidence,
        }

    def _predict_severity(self, detections: List[Dict[str, Any]]) -> tuple[SeverityLevel, float]:
        if not detections:
            return SeverityLevel.LOW, 0.2

        score = 0.0
        best_conf = 0.0
        for det in detections:
            weight = _CLASS_SEVERITY_WEIGHT.get(det["class_name"], 0.4)
            score += weight * det["confidence"]
            best_conf = max(best_conf, det["confidence"])

        avg_score = score / len(detections)

        if avg_score >= 0.7:
            level = SeverityLevel.CRITICAL
        elif avg_score >= 0.5:
            level = SeverityLevel.HIGH
        elif avg_score >= 0.3:
            level = SeverityLevel.MODERATE
        else:
            level = SeverityLevel.LOW

        return level, round(best_conf, 3)
