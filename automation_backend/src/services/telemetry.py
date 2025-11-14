import logging
from typing import List

from core.config import Settings
from core.models import TelemetryIngestRequest, TelemetryItem, TELEMETRY_BUFFER

logger = logging.getLogger(__name__)


class TelemetryService:
    """Service to ingest and retrieve telemetry data."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def _trim(self):
        overflow = max(0, len(TELEMETRY_BUFFER) - self.settings.TELEMETRY_BUFFER_SIZE)
        if overflow > 0:
            del TELEMETRY_BUFFER[0:overflow]

    # PUBLIC_INTERFACE
    def ingest(self, req: TelemetryIngestRequest) -> int:
        """Ingest telemetry items and return count added."""
        TELEMETRY_BUFFER.extend(req.items)
        self._trim()
        logger.info("Ingested %d telemetry items (buffer=%d)", len(req.items), len(TELEMETRY_BUFFER))
        return len(req.items)

    # PUBLIC_INTERFACE
    def last(self, n: int = 1) -> List[TelemetryItem]:
        """Return the last n telemetry items."""
        return TELEMETRY_BUFFER[-n:] if n > 0 else []

    # PUBLIC_INTERFACE
    def metrics(self) -> List[str]:
        """Return list of metric names currently seen in buffer."""
        names = sorted({item.metric for item in TELEMETRY_BUFFER})
        return names
