import os
import sys
import uvicorn

# PUBLIC_INTERFACE
def main():
    """
    Convenience entrypoint to start the FastAPI app with uvicorn ensuring a resolvable module path.

    This sets the app-dir to 'automation_backend/src' (relative to repo root) so that
    'src.api.main:app' can be imported correctly by uvicorn in preview environments.

    Usage examples (from repository root):
      - python -m src.api.preview_run
      - PYTHONPATH=automation_backend/src python -m src.api.preview_run

    It honors APP_HOST and APP_PORT environment variables via Settings defaults.
    """
    # Keep logs quiet for CI/preview
    os.environ.setdefault("ENABLE_DRY_RUN", "true")
    os.environ.setdefault("TIMEOUT_SECONDS", "1")
    os.environ.setdefault("LOG_LEVEL", "ERROR")

    # We will explicitly set the uvicorn app_dir so import path is resolvable for src.*
    # Compute the absolute app_dir path: <repo_root>/network-functional-testing-automation-192533-192542/automation_backend/src
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    app_dir = os.path.join(
        repo_root,
        "network-functional-testing-automation-192533-192542",
        "automation_backend",
        "src",
    )

    # As a fallback, also ensure PYTHONPATH contains app_dir
    sys.path.insert(0, app_dir)

    # Import settings and derive host/port
    try:
        from ..core.config import get_settings
        settings = get_settings()
        host = settings.APP_HOST
        port = settings.APP_PORT
    except Exception as exc:
        print(f"[preview_run] Failed to import settings: {exc}", file=sys.stderr)
        host, port = "0.0.0.0", 3001

    # Run uvicorn pointing at the module path and with app_dir set
    # Note: uvicorn.run supports 'app_dir' parameter to adjust module import base.
    uvicorn.run(
        "src.api.main:app",
        host=host,
        port=port,
        reload=False,
        app_dir=app_dir,
        log_level="error",
    )


if __name__ == "__main__":
    main()
