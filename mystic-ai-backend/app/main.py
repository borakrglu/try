"""
Mystic.ai Backend API
FastAPI application entry point
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import sentry_sdk
from contextlib import asynccontextmanager

from app.config import settings

# Initialize Sentry for error tracking
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.APP_ENV,
        traces_sample_rate=0.1 if settings.APP_ENV == "production" else 1.0,
    )

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events
    """
    # Startup
    print("🚀 Mystic.ai API starting up...")
    print(f"📍 Environment: {settings.APP_ENV}")
    print(f"🔧 Debug mode: {settings.DEBUG}")

    # TODO: Initialize database connection pool
    # TODO: Initialize Redis connection
    # TODO: Warm up AI models if needed

    yield

    # Shutdown
    print("👋 Mystic.ai API shutting down...")
    # TODO: Close database connections
    # TODO: Close Redis connections


# FastAPI app
app = FastAPI(
    title="Mystic.ai API",
    description="AI-powered mystical guidance platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.APP_ENV,
    }


# Root endpoint
@app.get("/")
async def root():
    """
    API root endpoint
    """
    return {
        "name": "Mystic.ai API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint not found"},
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# Include API routers
from app.api.v1 import auth, readings, upload, webhooks
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(readings.router, prefix="/api/v1/readings", tags=["Readings"])
app.include_router(upload.router, prefix="/api/v1/upload", tags=["Upload"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["Webhooks"])

# TODO: Add more routers as they're implemented
# app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
# app.include_router(journal.router, prefix="/api/v1/journal", tags=["Journal"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
