"""Convenience entrypoint: `python run.py` starts the API with uvicorn."""
import uvicorn

from config.settings import settings

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
