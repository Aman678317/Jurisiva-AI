# AI Run Logger & Observability Engine
# Records auditable metadata for every AI execution without persisting sensitive reasoning traces

import time
import uuid
from typing import Dict, List, Any, Optional

class AIRunLogger:
    """Immutable audit ledger for AI execution metadata, latency, tokens, and cost."""

    def __init__(self):
        self._runs: List[Dict[str, Any]] = []

    def start_run(
        self,
        org_id: str,
        case_id: str,
        user_id: str,
        workflow: str,
        model: str,
        provider: str,
        prompt_version: str = "v2.1",
        retrieval_version: str = "rag_hybrid_v1",
        tools_requested: Optional[List[str]] = None
    ) -> str:
        run_id = f"run_{uuid.uuid4().hex[:12]}"
        run_record = {
            "run_id": run_id,
            "org_id": org_id,
            "case_id": case_id,
            "user_id": user_id,
            "workflow": workflow,
            "model": model,
            "provider": provider,
            "prompt_version": prompt_version,
            "retrieval_version": retrieval_version,
            "tools_requested": tools_requested or [],
            "tools_executed": [],
            "start_time": time.time(),
            "end_time": None,
            "latency_ms": None,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "cost_usd": 0.0,
            "status": "RUNNING",
            "error": None
        }
        self._runs.append(run_record)
        return run_id

    def record_tool_execution(self, run_id: str, tool_name: str, status: str = "SUCCESS"):
        for r in self._runs:
            if r["run_id"] == run_id:
                r["tools_executed"].append({"tool": tool_name, "status": status, "timestamp": time.time()})
                break

    def complete_run(
        self,
        run_id: str,
        prompt_tokens: int,
        completion_tokens: int,
        cost_usd: float,
        status: str = "SUCCESS",
        error: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        for r in self._runs:
            if r["run_id"] == run_id:
                r["end_time"] = time.time()
                r["latency_ms"] = int((r["end_time"] - r["start_time"]) * 1000)
                r["prompt_tokens"] = prompt_tokens
                r["completion_tokens"] = completion_tokens
                r["total_tokens"] = prompt_tokens + completion_tokens
                r["cost_usd"] = round(cost_usd, 6)
                r["status"] = status
                r["error"] = error
                return r
        return None

    def get_runs(self, org_id: Optional[str] = None, case_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        results = self._runs
        if org_id:
            results = [r for r in results if r["org_id"] == org_id]
        if case_id:
            results = [r for r in results if r["case_id"] == case_id]
        return results[-limit:]

    def get_run_metrics(self, org_id: str) -> Dict[str, Any]:
        org_runs = [r for r in self._runs if r["org_id"] == org_id]
        total_tokens = sum(r["total_tokens"] for r in org_runs)
        total_cost = sum(r["cost_usd"] for r in org_runs)
        success_count = sum(1 for r in org_runs if r["status"] == "SUCCESS")
        return {
            "total_runs": len(org_runs),
            "success_rate": round(success_count / len(org_runs), 2) if org_runs else 1.0,
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost, 4),
            "average_latency_ms": int(sum(r["latency_ms"] or 0 for r in org_runs) / len(org_runs)) if org_runs else 0
        }

ai_run_logger = AIRunLogger()
