# AI API

## `POST /api/ai/detect` (multipart/form-data)
Field: `image`. Runs YOLO detection (or the mock fallback) and returns detections +
predicted severity + confidence.

## `POST /api/ai/chat`
```json
{ "message": "There's a fire near my building, what should I do?", "history": [] }
```
→ Gemini-generated (or fallback) safety guidance.
