"""Multi-language emergency instruction routes."""
from fastapi import APIRouter, Query

from services.translation_service import TranslationService
from utils.response import success_response

router = APIRouter(prefix="/translate", tags=["Translation"])


@router.get("/core-phrase", response_model=None)
async def core_phrase(key: str = Query(...), lang: str = Query("en")):
    service = TranslationService()
    text = service.translate_core_phrase(key, lang)
    return success_response({"key": key, "lang": lang, "text": text}, "Phrase fetched")


@router.post("/free-text", response_model=None)
async def free_text(text: str, target_lang: str):
    service = TranslationService()
    translated = await service.translate_free_text(text, target_lang)
    return success_response({"translated": translated}, "Text translated")
