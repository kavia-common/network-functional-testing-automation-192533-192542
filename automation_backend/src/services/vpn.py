import logging
from core.config import Settings
from core.models import VPNConnectRequest, VPNStatus
from utils.network import ping_host

logger = logging.getLogger(__name__)


class VpnService:
    """Service to manage VPN connectivity checks."""

    def __init__(self, settings: Settings):
        self.settings = settings

    # PUBLIC_INTERFACE
    def connect(self, req: VPNConnectRequest) -> VPNStatus:
        """Simulate VPN connect and return status."""
        logger.info("VPN connect profile=%s (dry_run=%s)", req.config_name, self.settings.ENABLE_DRY_RUN)
        ok, latency = ping_host(self.settings.VPN_CHECK_HOST, timeout=self.settings.TIMEOUT_SECONDS)
        return VPNStatus(connected=ok, check_host=self.settings.VPN_CHECK_HOST, latency_ms=latency)

    # PUBLIC_INTERFACE
    def status(self) -> VPNStatus:
        """Check current VPN status via reachability of check host."""
        ok, latency = ping_host(self.settings.VPN_CHECK_HOST, timeout=self.settings.TIMEOUT_SECONDS)
        logger.info("VPN status connected=%s latency=%.2fms", ok, latency)
        return VPNStatus(connected=ok, check_host=self.settings.VPN_CHECK_HOST, latency_ms=latency)
