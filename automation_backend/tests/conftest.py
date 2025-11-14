import os
import pytest
from fastapi.testclient import TestClient

# Ensure DRY RUN and short timeout for all tests
os.environ.setdefault("ENABLE_DRY_RUN", "true")
os.environ.setdefault("TIMEOUT_SECONDS", "1")
os.environ.setdefault("LOG_LEVEL", "ERROR")

# Import app after env vars are set so Settings pick them up
from src.api.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Provide a FastAPI TestClient for API tests."""
    return TestClient(app)


@pytest.fixture(scope="session")
def base_url() -> str:
    """Base API prefix for versioned endpoints."""
    return "/api/v1"
