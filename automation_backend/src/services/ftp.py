import logging
from src.core.config import Settings
from src.core.models import GenericAck, KeepAliveRequest

logger = logging.getLogger(__name__)


class FtpService:
    """Service to keep FTP session alive (stub)."""

    def __init__(self, settings: Settings):
        self.settings = settings

    # PUBLIC_INTERFACE
    def keepalive(self, req: KeepAliveRequest) -> GenericAck:
        """Perform a simple no-op to simulate an FTP keep-alive."""
        host = req.host or self.settings.FTP_HOST
        username = req.username or self.settings.FTP_USERNAME
        logger.info("FTP keepalive host=%s user=%s (dry_run=%s)", host, username, self.settings.ENABLE_DRY_RUN)
        return GenericAck(ok=True, message="FTP keepalive sent")
