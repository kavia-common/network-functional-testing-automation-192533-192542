import logging
from ..core.config import Settings
from ..core.models import GenericAck, VoipCallRequest

logger = logging.getLogger(__name__)


class VoipService:
    """Service integrating with a VOIP app in a dry-run/stubbed manner."""

    def __init__(self, settings: Settings):
        self.settings = settings

    # PUBLIC_INTERFACE
    def setup_call(self, req: VoipCallRequest) -> GenericAck:
        """Simulate setting up a VOIP call."""
        app_path = req.app_path or self.settings.VOIP_APP_PATH
        logger.info("VOIP setup to %s using app=%s (dry_run=%s)", req.callee, app_path, self.settings.ENABLE_DRY_RUN)
        return GenericAck(ok=True, message="VOIP call setup initiated")

    # PUBLIC_INTERFACE
    def teardown_call(self) -> GenericAck:
        """Simulate tearing down a VOIP call."""
        logger.info("VOIP call teardown (dry_run=%s)", self.settings.ENABLE_DRY_RUN)
        return GenericAck(ok=True, message="VOIP call teardown initiated")
