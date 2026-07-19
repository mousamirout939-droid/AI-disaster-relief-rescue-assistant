"""Business logic for direct AI endpoints: image detection and chatbot."""
from typing import Any, Dict, List

from services.ai_service import AIService
from services.gemini_service import GeminiService


async def analyze_image(ai_service: AIService, image_path: str) -> Dict[str, Any]:
    result = ai_service.analyze_report_image(image_path)
    return {
        "detections": result["detections"],
        "severity": result["severity"].value,
        "confidence": result["confidence"],
    }


async def chat_with_assistant(gemini_service: GeminiService, message: str, history: List[Dict[str, str]] | None = None) -> str:
    return await gemini_service.chat(message, history)
