import logging
import urllib.request
from src.core.config import Settings
from src.core.models import StreamingCheckRequest, StreamingCheckResult

logger = logging.getLogger(__name__)


class StreamingService:
    """Service to check streaming URL reachability."""

    def __init__(self, settings: Settings):
        self.settings = settings

    # PUBLIC_INTERFACE
    def check(self, req: StreamingCheckRequest) -> StreamingCheckResult:
        """Attempt to reach the stream URL with HEAD/GET, falling back to dry-run."""
        url = req.url or self.settings.STREAM_CHECK_URL
        reachable = True
        details = {"url": url, "dry_run": self.settings.ENABLE_DRY_RUN}
        if not self.settings.ENABLE_DRY_RUN:
            try:
                with urllib.request.urlopen(url, timeout=self.settings.TIMEOUT_SECONDS) as resp:
                    details["status"] = resp.status
            except Exception as exc:
                logger.warning("Streaming check failed: %s", exc)
                reachable = False
                details["error"] = str(exc)
        logger.info("Streaming reachable=%s url=%s", reachable, url)
        return StreamingCheckResult(url=url, reachable=reachable, details=details)
