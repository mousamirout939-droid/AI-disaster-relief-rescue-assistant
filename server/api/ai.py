"""Direct AI endpoints: standalone image detection + the Gemini emergency chatbot."""
from typing import List, Optional

from fastapi import APIRouter, Depends, File, UploadFile
from pydantic import BaseModel

from controllers import ai_controller
from dependencies.ai_dependency import get_gemini_service, get_yolo_service
from services.ai_service import AIService
from services.gemini_service import GeminiService
from services.yolo_service import YoloService
from utils.file_upload import save_upload_file
from utils.response import success_response

router = APIRouter(prefix="/ai", tags=["AI"])


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = None


@router.post("/detect", response_model=None)
async def detect_disaster(image: UploadFile = File(...), yolo: YoloService = Depends(get_yolo_service)):
    relative_url = await save_upload_file(image, subfolder="disaster_images")
    import pathlib
    absolute_path = str(pathlib.Path(__file__).resolve().parent.parent / relative_url.lstrip("/"))

    ai_service = AIService(yolo)
    data = await ai_controller.analyze_image(ai_service, absolute_path)
    data["image_url"] = relative_url
    return success_response(data, "Image analyzed")


@router.post("/chat", response_model=None)
async def chat(payload: ChatRequest, gemini: GeminiService = Depends(get_gemini_service)):
    reply = await ai_controller.chat_with_assistant(gemini, payload.message, payload.history)
    return success_response({"reply": reply}, "Chat response generated")
