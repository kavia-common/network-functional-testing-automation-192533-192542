import json
from fastapi.testclient import TestClient
from src.api.main import app


def generate_openapi_json(path: str = "interfaces/openapi.json"):
    """Generate the OpenAPI JSON for the FastAPI app to the interfaces folder."""
    client = TestClient(app)
    # Trigger schema build
    client.get("/openapi.json")
    schema = app.openapi()
    with open(path, "w") as f:
        json.dump(schema, f, indent=2)
    print(f"Wrote OpenAPI schema to {path}")


if __name__ == "__main__":
    generate_openapi_json()
