# Durable AIRun Logger Engine

import time
from typing import List, Dict, Optional

class AIRunLogger:
    def __init__(self):
        self._runs: List[Dict[str, Any]] = []

    def create_run(
        self,
        org_id: str,
        matter_id: str,
        user_id: str,
        workflow: str,
        model: str,
        prompt_version: str,
        retrieval_version: str = "v1"
    ) -> Dict[str, Any]:
        run_id = f"airun_{len(self._runs) + 1}"
        run_record = {
            "run_id": run_id,
            "organization_id": org_id,
            "matter_id": matter_id,
            "user_id": user_id,
            "workflow": workflow,
            "model": model,
            "prompt_version": prompt_version,
            "retrieval_version": retrieval_version,
            "status": "RUNNING",
            "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "completed_at": None,
            "latency_ms": 0,
            "tokens_used": 0,
            "cost_usd": 0.0,
            "error_code": None
        }
        self._runs.append(run_record)
        return run_record

    def complete_run(self, run_id: str, latency_ms: int, tokens_used: int, cost_usd: float) -> bool:
        for run in self._runs:
            if run["run_id"] == run_id:
                run["status"] = "COMPLETED"
                run["completed_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                run["latency_ms"] = latency_ms
                run["tokens_used"] = tokens_used
                run["cost_usd"] = cost_usd
                return True
        return False

ai_run_logger = AIRunLogger()
