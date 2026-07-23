"""
Simple in-memory sliding-window rate limiter middleware.
Skips OPTIONS requests so CORS preflight always succeeds.
"""

import time
from collections import defaultdict

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from config.settings import settings


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self._hits = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"

        now = time.time()
        window_start = now - settings.RATE_LIMIT_WINDOW_SECONDS

        hits = [t for t in self._hits[client_ip] if t > window_start]
        hits.append(now)
        self._hits[client_ip] = hits

        if len(hits) > settings.RATE_LIMIT_REQUESTS:
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "message": "Too many requests. Please slow down."
                },
            )

        return await call_next(request)