"""
Gemini API integration for the emergency AI chatbot.
Requires GEMINI_API_KEY in the environment. Falls back to canned safety
guidance if no key is configured, so the chatbot endpoint never hard-fails.
"""
from typing import List, Dict

import httpx

from config.settings import settings
from config.logging import logger

GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent"
)

SYSTEM_PROMPT = (
    "You are an emergency-response assistant embedded in a disaster relief app. "
    "Give calm, concise, actionable safety guidance. If the situation sounds "
    "life-threatening, tell the user to contact local emergency services "
    "immediately in addition to any advice you give."
)

_FALLBACK_REPLY = (
    "I can't reach the AI assistant right now (no Gemini API key configured). "
    "If this is an emergency, call your local emergency number immediately. "
    "For general safety: move to higher/open ground away from the hazard, "
    "avoid downed power lines and floodwater, and follow instructions from "
    "local authorities and the in-app emergency guides."
)


class GeminiService:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.GEMINI_API_KEY

    async def chat(self, message: str, history: List[Dict[str, str]] | None = None) -> str:
        if not self.api_key:
            return _FALLBACK_REPLY

        contents = [{"role": "user", "parts": [{"text": SYSTEM_PROMPT}]}]
        for turn in (history or [])[-10:]:
            contents.append({"role": turn.get("role", "user"), "parts": [{"text": turn.get("text", "")}]})
        contents.append({"role": "user", "parts": [{"text": message}]})

        try:
            async with httpx.AsyncClient(timeout=20) as client:
                resp = await client.post(
                    f"{GEMINI_ENDPOINT}?key={self.api_key}",
                    json={"contents": contents},
                )
                resp.raise_for_status()
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as exc:  # noqa: BLE001
            logger.error("Gemini API call failed: %s", exc)
            return _FALLBACK_REPLY
