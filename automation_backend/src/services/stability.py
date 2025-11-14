import logging
import threading
import time
import uuid
from datetime import datetime

from src.core.config import Settings
from src.core.models import JobInfo, JobStatus, JOBS, StabilityStartRequest

logger = logging.getLogger(__name__)


class StabilityService:
    """Service to manage stability test jobs."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def _worker(self, job_id: str, duration: int):
        logger.info("Stability job %s started for %ss", job_id, duration)
        try:
            JOBS[job_id].status = JobStatus.running
            JOBS[job_id].updated_at = datetime.utcnow()
            # Simulate work in intervals to keep responsive
            segments = max(1, duration // 2)
            for _ in range(segments):
                time.sleep(0.01 if self.settings.ENABLE_DRY_RUN else 1)
            JOBS[job_id].status = JobStatus.completed
            JOBS[job_id].message = "Completed successfully"
            JOBS[job_id].updated_at = datetime.utcnow()
            logger.info("Stability job %s completed", job_id)
        except Exception as exc:
            JOBS[job_id].status = JobStatus.failed
            JOBS[job_id].message = f"Failed: {exc}"
            JOBS[job_id].updated_at = datetime.utcnow()
            logger.exception("Stability job %s failed", job_id)

    # PUBLIC_INTERFACE
    def start(self, req: StabilityStartRequest) -> JobInfo:
        """Start a long-running stability job in background."""
        job_id = str(uuid.uuid4())
        job = JobInfo(
            id=job_id,
            status=JobStatus.pending,
            started_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            message=req.note,
        )
        JOBS[job_id] = job
        t = threading.Thread(target=self._worker, args=(job_id, req.duration_seconds), daemon=True)
        t.start()
        return job

    # PUBLIC_INTERFACE
    def status(self, job_id: str) -> JobInfo:
        """Get status for a stability job."""
        job = JOBS.get(job_id)
        if not job:
            raise KeyError("Job not found")
        return job
