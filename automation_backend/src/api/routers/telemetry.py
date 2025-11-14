from typing import List
from fastapi import APIRouter, Depends, Query, Body
from ..dependencies import get_telemetry_service
from ...core.models import TelemetryIngestRequest, TelemetryItem

router = APIRouter(prefix="/api/v1/telemetry", tags=["telemetry"])


@router.post("/ingest", summary="Ingest telemetry items", response_model=int)
def ingest(
    req: TelemetryIngestRequest = Body(..., embed=False),
    svc=Depends(get_telemetry_service),
) -> int:
    """Ingest one or more telemetry items, returning the number accepted."""
    return svc.ingest(req)


@router.get("/last", summary="Get last telemetry items", response_model=List[TelemetryItem])
def last(n: int = Query(1, description="Number of last items"), svc=Depends(get_telemetry_service)) -> List[TelemetryItem]:
    """Retrieve the last N telemetry items."""
    return svc.last(n)


@router.get("/metrics", summary="List metric names", response_model=List[str])
def metrics(svc=Depends(get_telemetry_service)) -> List[str]:
    """Retrieve list of metric names present in the buffer."""
    return svc.metrics()
