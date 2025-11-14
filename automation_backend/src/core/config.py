from functools import lru_cache
import logging
from pydantic import BaseSettings, Field, field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables with defaults."""
    APP_HOST: str = Field(default="0.0.0.0", description="Host to bind FastAPI app")
    APP_PORT: int = Field(default=3001, description="Port to bind FastAPI app")
    TIMEOUT_SECONDS: int = Field(default=10, description="Default network timeout in seconds")
    TRAFFIC_TEST_URL: str = Field(default="https://speed.hetzner.de/100MB.bin", description="Default URL for traffic download tests")
    VOIP_APP_PATH: str = Field(default="", description="Path to VOIP application for integration")
    FTP_HOST: str = Field(default="", description="FTP server hostname")
    FTP_USERNAME: str = Field(default="", description="FTP username")
    FTP_PASSWORD: str = Field(default="", description="FTP password")
    VPN_CHECK_HOST: str = Field(default="1.1.1.1", description="Host used to check VPN connectivity")
    STREAM_CHECK_URL: str = Field(default="https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", description="HLS stream URL to check streaming")
    TELEMETRY_BUFFER_SIZE: int = Field(default=1000, description="Max telemetry items kept in memory buffer")
    LOG_LEVEL: str = Field(default="INFO", description="Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL")
    ENABLE_DRY_RUN: bool = Field(default=True, description="If true, services will simulate actions without external side effects")

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        upper = v.upper()
        if upper not in valid:
            raise ValueError(f"LOG_LEVEL must be one of {valid}")
        return upper

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance and configure logging once based on LOG_LEVEL."""
    settings = Settings()
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    logging.getLogger("uvicorn").setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))
    return settings
