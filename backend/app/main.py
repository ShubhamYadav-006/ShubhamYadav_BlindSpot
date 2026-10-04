from contextlib import asynccontextmanager
import logging
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, Request, status
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
# pyrefly: ignore [missing-import]
from fastapi.responses import JSONResponse

from app.config import settings
from app.routes.analyze import router as analyze_router

logger = logging.getLogger("blind_spot.main")

# Max request body size: 50 KB (ample for 3000 chars decision + reasoning JSON payload)
MAX_REQUEST_BODY_BYTES = 50 * 1024


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Clean startup and shutdown logging banner."""
    print("\n" + "=" * 52)
    print("  🎯  BLIND SPOT API READY")
    print("=" * 52)
    print("  📍 Server:    http://127.0.0.1:8000")
    print("  💚 Health:    http://127.0.0.1:8000/health")
    print("  📖 API Docs:  http://127.0.0.1:8000/docs")
    print("=" * 52 + "\n")
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Blind Spot API - AI-powered decision-reflection engine",
    lifespan=lifespan,
)

# CORS middleware with explicit allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.middleware("http")
async def security_headers_and_size_limit_middleware(request: Request, call_next):
    """
    Applies security headers and enforces a maximum payload size threshold.
    """
    # 1. Payload size guard
    content_length = request.headers.get("content-length")
    if content_length:
        try:
            if int(content_length) > MAX_REQUEST_BODY_BYTES:
                return JSONResponse(
                    status_code=413,
                    content={"detail": "Request payload exceeds maximum allowed limit (50 KB)."},
                )
        except ValueError:
            pass

    # 2. Process request
    response = await call_next(request)

    # 3. Apply standard security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "accelerometer=(), camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = "default-src 'self'"

    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Top-level exception handler to ensure unhandled errors never leak tracebacks or secrets.
    """
    logger.error("Unhandled exception processing %s %s: %s", request.method, request.url.path, type(exc).__name__)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred while processing your request."},
    )


# Register routes
app.include_router(analyze_router)


@app.get("/health", summary="Health Check", tags=["System"])
def health_check() -> dict[str, str]:
    """Health check endpoint to verify backend operational readiness."""
    return {"status": "ok"}
