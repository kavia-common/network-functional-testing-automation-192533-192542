import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

# Import routers using the full 'src.' package path so uvicorn 'src.api.main:app' works consistently
from src.api.routers import health as health_router
from src.api.routers import tests as tests_router
from src.api.routers import telemetry as telemetry_router

logger = logging.getLogger(__name__)

# PUBLIC_INTERFACE
app = FastAPI(
    title="Network Functional Testing Automation API",
    description="FastAPI backend providing endpoints for traffic tests, VOIP integration, FTP keep-alive, VPN status, streaming checks, stability jobs, and telemetry ingestion.",
    version="1.0.0",
    openapi_tags=[
        {"name": "health", "description": "Health checks"},
        {"name": "tests", "description": "Network functional test endpoints"},
        {"name": "telemetry", "description": "Telemetry ingestion and queries"},
    ],
)
"""FastAPI application instance that registers health, tests, and telemetry routers."""

# Log detailed validation errors for 422 responses to aid debugging
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc: RequestValidationError):
    """
    Global handler to log detailed validation errors.

    Logs the request path, method, and the validation errors for easier diagnosis
    of 422 Unprocessable Entity issues during development and CI runs.
    """
    logger.error(
        "Validation error on %s %s | errors=%s",
        getattr(request, "method", "UNKNOWN"),
        getattr(request, "url", "UNKNOWN"),
        exc.errors(),
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root and /health are provided in health router; include router to provide them at root.
app.include_router(health_router.router)
# Versioned routers
app.include_router(tests_router.router)
app.include_router(telemetry_router.router)
