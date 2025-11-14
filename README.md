# network-functional-testing-automation-192533-192542

Automation backend providing FastAPI endpoints for network functional testing (traffic, VOIP, FTP, VPN, streaming, stability) and telemetry ingestion.

## Run locally

- Install dependencies (Python 3.11+ recommended):
  pip install -r automation_backend/requirements.txt

- Start app (recommended for preview runners and CI):
  uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload --app-dir automation_backend/src

- Alternative (uses APP_HOST/APP_PORT from .env or defaults: 0.0.0.0:3001):
  PYTHONPATH=automation_backend/src python -m src.api.run

- Preview helper (ensures correct app-dir automatically):
  PYTHONPATH=automation_backend/src python -m src.api.preview_run

Docs: http://localhost:3001/docs
OpenAPI JSON: http://localhost:3001/openapi.json

## Generate OpenAPI file

From the container root directory:
  python -m src.api.generate_openapi --module src.api.generate_openapi

Or:
  PYTHONPATH=automation_backend/src python automation_backend/src/api/generate_openapi.py

This will write interfaces/openapi.json.

## Environment variables

Supported variables (with defaults):

- APP_HOST=0.0.0.0
- APP_PORT=3001
- TIMEOUT_SECONDS=10
- TRAFFIC_TEST_URL=https://speed.hetzner.de/100MB.bin
- VOIP_APP_PATH=""
- FTP_HOST=""
- FTP_USERNAME=""
- FTP_PASSWORD=""
- VPN_CHECK_HOST=1.1.1.1
- STREAM_CHECK_URL=https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8
- TELEMETRY_BUFFER_SIZE=1000
- LOG_LEVEL=INFO
- ENABLE_DRY_RUN=true

Set these in an .env file at automation_backend/.env (do not commit secrets).

## Endpoints overview

- Health:
  - GET /, GET /health, GET /api/v1/health

- Tests (prefix /api/v1/tests):
  - POST /traffic/upload
  - POST /traffic/download
  - POST /voip/call/setup
  - POST /voip/call/teardown
  - POST /ftp/keepalive
  - POST /vpn/connect
  - POST /vpn/status
  - POST /streaming/check
  - POST /stability/start
  - GET  /stability/status?id=JOB_ID
  - GET  /{id}/result

- Telemetry (prefix /api/v1/telemetry):
  - POST /ingest
  - GET  /last?n=10
  - GET  /metrics

## Notes

- Services implement dry-run behavior to be CI-friendly and avoid external side effects.
- In-memory registries are used for demo: job status, test results, and telemetry buffer.
- LOG_LEVEL controls logging verbosity.