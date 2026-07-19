# `file/` (legacy duplicate folder)

The original skeleton also included this `file/` directory alongside
`server/ai_model/` and `server/services/yolo_service.py` / `ai_service.py`
for the same disaster-detection AI pipeline. To keep a single source of
truth, this folder re-exports the real implementation rather than
duplicating logic. Use `server/services/` and `server/ai_model/` directly
when building on this project.
