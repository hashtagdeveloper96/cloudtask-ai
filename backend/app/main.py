from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.debug import router as debug_router
from app.api.v1.health import router as health_router
from app.api.v1.tasks import router as tasks_router
from app.api.v1.metrics import router as metrics_router
from app.core.metrics import PrometheusMiddleware
from app.api.v1.readiness import router as readiness_router
from app.core.config import get_settings
from app.core.exceptions import global_exception_handler
from app.core.logging_config import configure_logging
from app.core.middleware import RequestLoggingMiddleware


# ---------------------------------------------------------
# Application configuration
# ---------------------------------------------------------

settings = get_settings()

configure_logging()


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "CloudTask AI API - "
        "Task management platform with authentication, "
        "authorization, PostgreSQL, Docker, logging, "
        "monitoring and AI capabilities."
    ),
)


# ---------------------------------------------------------
# Middleware
# ---------------------------------------------------------

app.add_middleware(
    RequestLoggingMiddleware
)

app.add_middleware(
    PrometheusMiddleware
)


# ---------------------------------------------------------
# Global exception handling
# ---------------------------------------------------------

app.add_exception_handler(
    Exception,
    global_exception_handler,
)


app.include_router(
    readiness_router,
    prefix="/api/v1",
)

# ---------------------------------------------------------
# API Routers
# ---------------------------------------------------------

app.include_router(
    health_router,
    prefix="/api/v1",
)

app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    tasks_router,
    prefix="/api/v1",
)

app.include_router(
    debug_router,
    prefix="/api/v1",
)

app.include_router(metrics_router)

# ---------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------

@app.get(
    "/",
    tags=["Root"],
)
def root():
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "running",
        "docs": "/docs",
    }
