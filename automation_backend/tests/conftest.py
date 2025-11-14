import os
import sys
import pathlib
import pytest
from fastapi.testclient import TestClient

# Ensure DRY RUN and short timeout for all tests
os.environ.setdefault("ENABLE_DRY_RUN", "true")
os.environ.setdefault("TIMEOUT_SECONDS", "1")
os.environ.setdefault("LOG_LEVEL", "ERROR")

# Ensure the src package is importable when running via pytest
# This inserts '<container_root>/src' (automation_backend/src) into sys.path.
_here = pathlib.Path(__file__).resolve()
_container_root = _here.parents[1]  # automation_backend/
_src_path = _container_root / "src"
if str(_src_path) not in sys.path:
    sys.path.insert(0, str(_src_path))

# Import app after env vars and path are set so Settings pick them up
from src.api.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Provide a FastAPI TestClient for API tests."""
    return TestClient(app)


@pytest.fixture(scope="session")
def base_url() -> str:
    """Base API prefix for versioned endpoints."""
    return "/api/v1"
