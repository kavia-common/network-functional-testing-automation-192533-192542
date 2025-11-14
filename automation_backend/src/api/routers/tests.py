from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import (
    get_traffic_service,
    get_voip_service,
    get_ftp_service,
    get_vpn_service,
    get_streaming_service,
    get_stability_service,
)
from ...core.models import (
    TrafficRequest,
    TrafficResult,
    VoipCallRequest,
    GenericAck,
    KeepAliveRequest,
    VPNConnectRequest,
    VPNStatus,
    StreamingCheckRequest,
    StreamingCheckResult,
    StabilityStartRequest,
    JobInfo,
)

router = APIRouter(prefix="/api/v1/tests", tags=["tests"])


@router.post("/traffic/upload", summary="Run upload traffic test", response_model=TrafficResult)
def traffic_upload(
    request: TrafficRequest,
    svc=Depends(get_traffic_service),
) -> TrafficResult:
    """Run an upload traffic test and return result."""
    return svc.upload(request)


@router.post("/traffic/download", summary="Run download traffic test", response_model=TrafficResult)
def traffic_download(
    request: TrafficRequest,
    svc=Depends(get_traffic_service),
) -> TrafficResult:
    """Run a download traffic test and return result."""
    return svc.download(request)


@router.post("/voip/call/setup", summary="Setup VOIP call", response_model=GenericAck)
def voip_setup(
    request: VoipCallRequest,
    svc=Depends(get_voip_service),
) -> GenericAck:
    """Initiate a VOIP call setup."""
    return svc.setup_call(request)


@router.post("/voip/call/teardown", summary="Teardown VOIP call", response_model=GenericAck)
def voip_teardown(svc=Depends(get_voip_service)) -> GenericAck:
    """Teardown VOIP call."""
    return svc.teardown_call()


@router.post("/ftp/keepalive", summary="Send FTP keepalive", response_model=GenericAck)
def ftp_keepalive(
    request: KeepAliveRequest,
    svc=Depends(get_ftp_service),
) -> GenericAck:
    """Perform FTP keep-alive operation."""
    return svc.keepalive(request)


@router.post("/vpn/connect", summary="Connect VPN", response_model=VPNStatus)
def vpn_connect(
    request: VPNConnectRequest,
    svc=Depends(get_vpn_service),
) -> VPNStatus:
    """Simulate VPN connect and check status."""
    return svc.connect(request)


@router.post("/vpn/status", summary="VPN status", response_model=VPNStatus)
def vpn_status(svc=Depends(get_vpn_service)) -> VPNStatus:
    """Get current VPN status."""
    return svc.status()


@router.post("/streaming/check", summary="Check streaming URL", response_model=StreamingCheckResult)
def streaming_check(
    request: StreamingCheckRequest,
    svc=Depends(get_streaming_service),
) -> StreamingCheckResult:
    """Check streaming URL reachability."""
    return svc.check(request)


@router.post("/stability/start", summary="Start stability test", response_model=JobInfo)
def stability_start(
    request: StabilityStartRequest,
    svc=Depends(get_stability_service),
) -> JobInfo:
    """Start a background stability test job."""
    return svc.start(request)


@router.get("/stability/status", summary="Get stability job status", response_model=JobInfo)
def stability_status(id: str, svc=Depends(get_stability_service)) -> JobInfo:
    """Get stability job status by id."""
    try:
        return svc.status(id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Job not found")


@router.get("/{id}/result", summary="Get test result by id", response_model=TrafficResult)
def get_test_result(id: str, svc=Depends(get_traffic_service)) -> TrafficResult:
    """Get stored test result by id."""
    result = svc.get_result(id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result
