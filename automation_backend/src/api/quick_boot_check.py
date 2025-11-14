import os
import threading
import time
import socket
import sys

import http.client

# Ensure minimal noisy logs and fast responses
os.environ.setdefault("ENABLE_DRY_RUN", "true")
os.environ.setdefault("TIMEOUT_SECONDS", "1")
os.environ.setdefault("LOG_LEVEL", "ERROR")

# PUBLIC_INTERFACE
def run_quick_boot_check(timeout: float = 5.0) -> int:
    """
    Launch the FastAPI app with uvicorn in a background thread, wait for port readiness,
    then verify GET / and GET /api/v1/health return HTTP 200. Returns exit code (0 on success).
    """
    try:
        import uvicorn
        from ..core.config import get_settings
        # Import app to validate import path, but we will launch via uvicorn programmatically
        from .main import app  # noqa: F401
    except Exception as exc:
        print(f"[quick_boot_check] Import failed: {exc}", file=sys.stderr)
        return 2

    settings = get_settings()
    host = settings.APP_HOST
    port = settings.APP_PORT

    # Start uvicorn server in a separate thread
    config = uvicorn.Config("src.api.main:app", host=host, port=port, log_level="error")
    server = uvicorn.Server(config=config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    # Wait for port ready
    deadline = time.time() + timeout
    def is_port_open(h: str, p: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.25)
            try:
                s.connect((h, p))
                return True
            except Exception:
                return False

    while time.time() < deadline:
        if is_port_open(host, port):
            break
        time.sleep(0.05)
    else:
        print(f"[quick_boot_check] Port {host}:{port} did not open within {timeout}s", file=sys.stderr)
        return 3

    # Simple HTTP checks
    def get_status(path: str) -> int:
        try:
            conn = http.client.HTTPConnection(host, port, timeout=1.5)
            conn.request("GET", path)
            resp = conn.getresponse()
            status = resp.status
            resp.read()  # drain
            conn.close()
            return status
        except Exception as e:
            print(f"[quick_boot_check] Request to {path} failed: {e}", file=sys.stderr)
            return 0

    root_status = get_status("/")
    api_health_status = get_status("/api/v1/health")

    # Attempt graceful shutdown
    try:
        server.should_exit = True
    except Exception:
        pass

    if root_status != 200:
        print(f"[quick_boot_check] GET / returned {root_status}, expected 200", file=sys.stderr)
        return 4
    if api_health_status != 200:
        print(f"[quick_boot_check] GET /api/v1/health returned {api_health_status}, expected 200", file=sys.stderr)
        return 5

    print("[quick_boot_check] OK: root and /api/v1/health returned 200")
    return 0


if __name__ == "__main__":
    code = run_quick_boot_check()
    sys.exit(code)
