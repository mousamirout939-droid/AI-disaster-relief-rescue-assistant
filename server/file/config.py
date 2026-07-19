"""Re-export of the app-wide AI configuration values."""
from config.settings import settings  # noqa: F401

YOLO_WEIGHTS_PATH = settings.YOLO_WEIGHTS_PATH
CONFIDENCE_THRESHOLD = settings.YOLO_CONFIDENCE_THRESHOLD
