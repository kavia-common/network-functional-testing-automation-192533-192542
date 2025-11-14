from functools import lru_cache

from ..core.config import Settings, get_settings
from ..services.traffic import TrafficService
from ..services.voip import VoipService
from ..services.ftp import FtpService
from ..services.vpn import VpnService
from ..services.streaming import StreamingService
from ..services.stability import StabilityService
from ..services.telemetry import TelemetryService


@lru_cache
def get_settings_dep() -> Settings:
    """Provide cached settings instance."""
    return get_settings()


def get_traffic_service(settings: Settings = None) -> TrafficService:
    """Return traffic service wired with settings."""
    settings = settings or get_settings_dep()
    return TrafficService(settings)


def get_voip_service(settings: Settings = None) -> VoipService:
    """Return VOIP service wired with settings."""
    settings = settings or get_settings_dep()
    return VoipService(settings)


def get_ftp_service(settings: Settings = None) -> FtpService:
    """Return FTP service wired with settings."""
    settings = settings or get_settings_dep()
    return FtpService(settings)


def get_vpn_service(settings: Settings = None) -> VpnService:
    """Return VPN service wired with settings."""
    settings = settings or get_settings_dep()
    return VpnService(settings)


def get_streaming_service(settings: Settings = None) -> StreamingService:
    """Return streaming service wired with settings."""
    settings = settings or get_settings_dep()
    return StreamingService(settings)


def get_stability_service(settings: Settings = None) -> StabilityService:
    """Return stability service wired with settings."""
    settings = settings or get_settings_dep()
    return StabilityService(settings)


def get_telemetry_service(settings: Settings = None) -> TelemetryService:
    """Return telemetry service wired with settings."""
    settings = settings or get_settings_dep()
    return TelemetryService(settings)
