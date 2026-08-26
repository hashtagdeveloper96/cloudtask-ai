from fastapi import APIRouter

from app.core.config import get_settings


router = APIRouter(
    tags=["Health"],
)


@router.get("/ready")
def readiness_check():
    settings = get_settings()

    return {
        "status": "ready",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }
