import logging
import time
import uuid
from datetime import datetime

from core.config import Settings
from core.models import TrafficRequest, TrafficResult, TEST_RESULTS

logger = logging.getLogger(__name__)


class TrafficService:
    """Service for traffic upload/download tests."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def _simulate_transfer(self, direction: str, req: TrafficRequest) -> TrafficResult:
        started = datetime.utcnow()
        # Simulate network transfer timing based on size or duration
        time.sleep(0.01 if self.settings.ENABLE_DRY_RUN else 0.1)
        mbps = 100.0 if self.settings.ENABLE_DRY_RUN else 50.0
        finished = datetime.utcnow()
        test_id = str(uuid.uuid4())
        result = TrafficResult(
            id=test_id,
            direction=direction,
            success=True,
            throughput_mbps=mbps,
            started_at=started,
            finished_at=finished,
            details={
                "target_url": req.target_url or self.settings.TRAFFIC_TEST_URL,
                "bytes": req.bytes or 0,
                "duration_seconds": req.duration_seconds or 0,
                "dry_run": self.settings.ENABLE_DRY_RUN,
            },
        )
        TEST_RESULTS[test_id] = result
        logger.info("Traffic %s completed: %s Mbps id=%s", direction, mbps, test_id)
        return result

    # PUBLIC_INTERFACE
    def upload(self, req: TrafficRequest) -> TrafficResult:
        """Perform a traffic upload test and return the result."""
        return self._simulate_transfer("upload", req)

    # PUBLIC_INTERFACE
    def download(self, req: TrafficRequest) -> TrafficResult:
        """Perform a traffic download test and return the result."""
        return self._simulate_transfer("download", req)

    # PUBLIC_INTERFACE
    def get_result(self, test_id: str) -> TrafficResult | None:
        """Get a previously stored test result by id."""
        return TEST_RESULTS.get(test_id)
