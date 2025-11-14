import uvicorn
from core.config import get_settings

# PUBLIC_INTERFACE
def main():
    """
    Entrypoint to run the FastAPI app with uvicorn using configured host/port.

    Reads APP_HOST and APP_PORT from environment via Settings (defaults: 0.0.0.0:3001).
    """
    settings = get_settings()
    uvicorn.run(
        "src.api.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=False,
        app_dir=None,
        # Use HTTP/1.1 loop, not websockets extras, for simplicity in CI
    )


if __name__ == "__main__":
    main()
