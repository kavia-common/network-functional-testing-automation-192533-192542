"""
Utility script to verify that the FastAPI app is importable.

Usage:
  PYTHONPATH=automation_backend/src python -m src.api.import_check
or from the container root:
  PYTHONPATH=automation_backend/src python network-functional-testing-automation-192533-192542/automation_backend/src/api/import_check.py
"""
import os
import traceback

# help ensure clean minimal config for CI import
os.environ.setdefault("ENABLE_DRY_RUN", "true")
os.environ.setdefault("TIMEOUT_SECONDS", "1")
os.environ.setdefault("LOG_LEVEL", "ERROR")

# PUBLIC_INTERFACE
def check() -> bool:
    """Attempt to import the FastAPI app and return True on success."""
    try:
        from src.api.main import app  # noqa: F401
        return True
    except Exception as exc:
        print(f"Import failed: {exc}")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    ok = check()
    print("OK" if ok else "FAIL")
