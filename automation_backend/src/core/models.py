from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class HealthResponse(BaseModel):
    status: str = Field(..., description="Overall health status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Server time in UTC")


class TrafficRequest(BaseModel):
    target_url: Optional[str] = Field(None, description="Override URL to use for traffic test")
    duration_seconds: Optional[int] = Field(None, description="Optional duration for the test")
    bytes: Optional[int] = Field(None, description="Optional byte size to upload/download")


class TrafficResult(BaseModel):
    id: str = Field(..., description="Job id")
    direction: str = Field(..., description="upload or download")
    success: bool = Field(..., description="Whether the test succeeded")
    throughput_mbps: float = Field(..., description="Measured throughput in Mbps")
    started_at: datetime = Field(..., description="Start time")
    finished_at: datetime = Field(..., description="Finish time")
    details: Dict[str, Any] = Field(default_factory=dict, description="Additional details")


class VoipCallRequest(BaseModel):
    callee: Optional[str] = Field(None, description="Callee identifier or number")
    app_path: Optional[str] = Field(None, description="Override path to VOIP app")


class GenericAck(BaseModel):
    ok: bool = Field(..., description="Whether the request was accepted")
    message: str = Field(..., description="Additional message")


class KeepAliveRequest(BaseModel):
    host: Optional[str] = Field(None, description="FTP host override")
    username: Optional[str] = Field(None, description="FTP username override")
    password: Optional[str] = Field(None, description="FTP password override")
    interval_seconds: Optional[int] = Field(None, description="Interval between keep-alive operations")


class VPNConnectRequest(BaseModel):
    config_name: Optional[str] = Field(None, description="VPN configuration name or profile")


class VPNStatus(BaseModel):
    connected: bool = Field(..., description="Whether VPN is connected")
    check_host: str = Field(..., description="Host used for connectivity check")
    latency_ms: Optional[float] = Field(None, description="Estimated latency in ms")


class StreamingCheckRequest(BaseModel):
    url: Optional[str] = Field(None, description="Streaming URL override to check")


class StreamingCheckResult(BaseModel):
    url: str = Field(..., description="Checked streaming URL")
    reachable: bool = Field(..., description="Whether stream is reachable")
    details: Dict[str, Any] = Field(default_factory=dict, description="Extra details")


class StabilityStartRequest(BaseModel):
    duration_seconds: int = Field(..., description="How long to run the stability test")
    note: Optional[str] = Field(None, description="Optional note for the job")


class JobInfo(BaseModel):
    id: str = Field(..., description="Job id")
    status: JobStatus = Field(..., description="Status of the job")
    started_at: datetime = Field(..., description="Start time")
    updated_at: datetime = Field(..., description="Last update time")
    message: Optional[str] = Field(None, description="Status message")


class TelemetryItem(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Telemetry time")
    metric: str = Field(..., description="Metric name")
    value: float = Field(..., description="Metric value")
    tags: Dict[str, str] = Field(default_factory=dict, description="Arbitrary tags")


class TelemetryIngestRequest(BaseModel):
    items: List[TelemetryItem] = Field(..., description="List of telemetry items to ingest")


# In-memory registries for demonstration purposes
TEST_RESULTS: Dict[str, TrafficResult] = {}
JOBS: Dict[str, JobInfo] = {}
TELEMETRY_BUFFER: List[TelemetryItem] = []
