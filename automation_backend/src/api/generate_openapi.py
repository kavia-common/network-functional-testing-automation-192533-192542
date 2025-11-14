from fastapi.encoders import jsonable_encoder
from src.api.main import app
import json
import os

# PUBLIC_INTERFACE
def generate_openapi_file(output_path: str = None):
    """
    Generate and write the OpenAPI schema for the FastAPI app.

    Parameters:
    - output_path: Optional path to write the OpenAPI JSON. If not provided,
      defaults to project 'interfaces/openapi.json' relative to container root.

    Returns:
    - The path where the OpenAPI schema was written.
    """
    schema = app.openapi()
    data = jsonable_encoder(schema)
    if output_path is None:
        # Resolve to the container's interfaces directory
        here = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        # here -> automation_backend/src
        container_root = os.path.dirname(here)  # automation_backend
        output_path = os.path.join(container_root, "interfaces", "openapi.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return output_path


if __name__ == "__main__":
    path = generate_openapi_file()
    print(f"OpenAPI schema written to: {path}")
