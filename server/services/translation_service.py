"""
Emergency instruction translation service.
Ships a small built-in phrase dictionary for offline-safe core guidance, and
optionally calls Gemini for free-form translation when an API key is set.
"""
from typing import Dict

from services.gemini_service import GeminiService

_CORE_PHRASES: Dict[str, Dict[str, str]] = {
    "stay_calm_move_to_safety": {
        "en": "Stay calm and move to higher/open ground away from the hazard.",
        "hi": "शांत रहें और खतरे से दूर ऊँची/खुली जगह की ओर बढ़ें।",
        "kn": "ಶಾಂತವಾಗಿರಿ ಮತ್ತು ಅಪಾಯದಿಂದ ದೂರ ಎತ್ತರದ/ತೆರೆದ ಸ್ಥಳಕ್ಕೆ ಹೋಗಿ.",
        "es": "Mantén la calma y muévete a un terreno alto y abierto lejos del peligro.",
    },
    "call_emergency_services": {
        "en": "Call local emergency services immediately.",
        "hi": "तुरंत स्थानीय आपातकालीन सेवाओं को कॉल करें।",
        "kn": "ತಕ್ಷಣ ಸ್ಥಳೀಯ ತುರ್ತು ಸೇವೆಗಳಿಗೆ ಕರೆ ಮಾಡಿ.",
        "es": "Llama de inmediato a los servicios de emergencia locales.",
    },
}


class TranslationService:
    def __init__(self):
        self.gemini = GeminiService()

    def translate_core_phrase(self, key: str, lang: str) -> str:
        phrase = _CORE_PHRASES.get(key, {})
        return phrase.get(lang) or phrase.get("en", "")

    async def translate_free_text(self, text: str, target_lang: str) -> str:
        prompt = f"Translate the following emergency instruction into language code '{target_lang}'. Return only the translation:\n\n{text}"
        return await self.gemini.chat(prompt)
