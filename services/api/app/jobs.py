# Asynchronous Processing Job State Machine

from typing import Dict, Optional

VALID_JOB_TRANSITIONS = {
    "QUEUED": {"VALIDATING", "CANCELLED"},
    "VALIDATING": {"EXTRACTING", "FAILED"},
    "EXTRACTING": {"OCR_PENDING", "FAILED"},
    "OCR_PENDING": {"OCR_RUNNING", "FAILED"},
    "OCR_RUNNING": {"INDEXING_PENDING", "FAILED"},
    "INDEXING_PENDING": {"READY", "NEEDS_REVIEW", "FAILED"},
    "FAILED": {"QUEUED"}, // Allows bounded retry transition
    "READY": set(),
}

class JobStateEngine:
    def __init__(self):
        self._jobs: Dict[str, Dict] = {}

    def create_job(self, org_id: str, matter_id: str, doc_id: str, job_type: str = "DOCUMENT_INGESTION") -> Dict:
        job_id = f"job_{len(self._jobs) + 1}"
        job = {
            "job_id": job_id,
            "organization_id": org_id,
            "matter_id": matter_id,
            "document_id": doc_id,
            "job_type": job_type,
            "status": "QUEUED",
            "attempt_count": 0,
            "max_attempts": 3,
            "error_code": None,
            "progress": 0.0,
        }
        self._jobs[job_id] = job
        return job

    def transition_state(self, job_id: str, target_state: str, error_code: Optional[str] = None) -> tuple[bool, str]:
        job = self._jobs.get(job_id)
        if not job:
            return False, "JOB_NOT_FOUND"

        current_state = job["status"]
        allowed = VALID_JOB_TRANSITIONS.get(current_state, set())

        if target_state not in allowed:
            return False, f"INVALID_TRANSITION: Cannot transition from {current_state} to {target_state}"

        job["status"] = target_state
        if error_code:
            job["error_code"] = error_code
        return True, "SUCCESS"

    def get_job(self, job_id: str) -> Optional[Dict]:
        return self._jobs.get(job_id)

job_engine = JobStateEngine()
