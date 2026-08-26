from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.api.v1.readiness import router as readiness_router
from app.core.config import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="AI-powered cloud task management platform",
    version=settings.app_version,
    debug=settings.debug,
)

app.include_router(
    health_router,
    prefix="/api/v1",
)

app.include_router(
    readiness_router,
    prefix="/api/v1",
)
