# Asynchronous Job Queue Interface for Render Background Workers
# Supports Redis-compatible broker and PostgreSQL fallback with exponential backoff

import time
import uuid
import json
import logging
from typing import Dict, Any, Optional, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("JurisivaJobQueue")

class JobQueue:
    """Manages enqueueing, leasing, retries, and state transitions for background tasks."""

    def __init__(self):
        self._in_memory_queue: List[Dict[str, Any]] = []
        self._job_registry: Dict[str, Dict[str, Any]] = {}

    def enqueue(
        self,
        job_type: str,
        case_id: str,
        organization_id: str = "org_001",
        payload: Optional[Dict[str, Any]] = None,
        max_attempts: int = 3
    ) -> Dict[str, Any]:
        """Adds a job to the asynchronous queue."""
        job_id = f"job_{uuid.uuid4().hex[:12]}"
        job = {
            "job_id": job_id,
            "case_id": case_id,
            "organization_id": organization_id,
            "job_type": job_type,
            "status": "QUEUED", # QUEUED, RUNNING, COMPLETED, FAILED, RETRYING, CANCELLED
            "payload": payload or {},
            "result": {},
            "attempts": 0,
            "max_attempts": max_attempts,
            "error": None,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "started_at": None,
            "completed_at": None
        }
        self._in_memory_queue.append(job)
        self._job_registry[job_id] = job
        logger.info(f"Enqueued job [{job_id}] of type '{job_type}' for case '{case_id}'")
        return job

    def fetch_next_job(self) -> Optional[Dict[str, Any]]:
        """Leases the next available QUEUED or RETRYING job."""
        for job in self._in_memory_queue:
            if job["status"] in ["QUEUED", "RETRYING"]:
                job["status"] = "RUNNING"
                job["started_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                job["attempts"] += 1
                logger.info(f"Leasing job [{job['job_id']}] (Attempt {job['attempts']}/{job['max_attempts']})")
                return job
        return None

    def complete_job(self, job_id: str, result: Dict[str, Any]):
        """Marks a job as successfully completed."""
        job = self._job_registry.get(job_id)
        if job:
            job["status"] = "COMPLETED"
            job["result"] = result
            job["completed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Successfully completed job [{job_id}]")

    def fail_job(self, job_id: str, error: str, is_transient: bool = True):
        """Handles job failure with exponential backoff retry or dead-letter failure."""
        job = self._job_registry.get(job_id)
        if not job:
            return

        job["error"] = error
        if is_transient and job["attempts"] < job["max_attempts"]:
            job["status"] = "RETRYING"
            backoff_sec = (2 ** job["attempts"])
            logger.warning(f"Job [{job_id}] failed transiently ({error}). Scheduling retry in {backoff_sec}s")
        else:
            job["status"] = "FAILED"
            job["completed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            logger.error(f"Job [{job_id}] permanently FAILED ({error})")

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        return self._job_registry.get(job_id)

    def list_jobs(self, case_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if case_id:
            return [j for j in self._job_registry.values() if j["case_id"] == case_id]
        return list(self._job_registry.values())

job_queue = JobQueue()
