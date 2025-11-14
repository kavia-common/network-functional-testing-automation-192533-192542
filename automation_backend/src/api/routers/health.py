from datetime import datetime
from fastapi import APIRouter
from ...core.models import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/", summary="Health Check (root)", description="Root endpoint to validate the service is up.")
def root_health() -> HealthResponse:
    """Return a simple health response at root."""
    return HealthResponse(status="ok", timestamp=datetime.utcnow())


@router.get("/health", summary="Health Check", description="Explicit health endpoint at root.")
def health() -> HealthResponse:
    """Return health status at /health."""
    return HealthResponse(status="ok", timestamp=datetime.utcnow())


# Also provide versioned health under /api/v1 via include_router prefix in main.
@router.get("/api/v1/health", summary="API v1 Health", description="Health endpoint under /api/v1.")
def api_v1_health() -> HealthResponse:
    """Return health status for API v1."""
    return HealthResponse(status="ok", timestamp=datetime.utcnow())
