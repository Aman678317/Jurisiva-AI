# Dead Letter Queue & Asynchronous Job Recovery Engine

import time
from typing import Dict, List, Any

class DeadLetterQueueManager:
    """Stores failed asynchronous jobs for operator inspection, quarantine, and safe replay."""

    def __init__(self):
        self._dlq_records: List[Dict[str, Any]] = []

    def quarantine_failed_job(self, job_id: str, service: str, payload_ref: str, failure_reason: str, attempts: int) -> Dict[str, Any]:
        record = {
            "job_id": job_id,
            "service": service,
            "payload_ref": payload_ref,
            "failure_reason": failure_reason,
            "attempts": attempts,
            "quarantined_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "status": "QUARANTINED"
        }
        self._dlq_records.append(record)
        return record

    def replay_job(self, job_id: str) -> Dict[str, Any]:
        for rec in self._dlq_records:
            if rec["job_id"] == job_id and rec["status"] == "QUARANTINED":
                rec["status"] = "REPLAY_QUEUED"
                rec["replayed_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                return {"status": "SUCCESS", "job": rec}
        return {"status": "NOT_FOUND", "reason": "Job ID not found or not in QUARANTINED state."}

dlq_manager = DeadLetterQueueManager()
