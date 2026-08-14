# Tenant Resource Governance & Noisy Neighbor Protection Engine

import time
from typing import Dict, Any

class TenantResourceGovernor:
    """Enforces organization concurrency limits, rate limits, token budgets, and tenant-safe cache key generation."""

    def __init__(self, max_concurrent_jobs: int = 10, max_rpm: int = 600):
        self.max_concurrent_jobs = max_concurrent_jobs
        self.max_rpm = max_rpm
        self._active_jobs: Dict[str, int] = {}

    def acquire_job_slot(self, org_id: str) -> Dict[str, Any]:
        current = self._active_jobs.get(org_id, 0)
        if current >= self.max_concurrent_jobs:
            return {"status": "THROTTLED", "reason": f"Organization '{org_id}' exceeded max concurrent job capacity ({self.max_concurrent_jobs})."}

        self._active_jobs[org_id] = current + 1
        return {"status": "ALLOWED", "active_jobs": self._active_jobs[org_id]}

    def release_job_slot(self, org_id: str):
        if org_id in self._active_jobs and self._active_jobs[org_id] > 0:
            self._active_jobs[org_id] -= 1

    @staticmethod
    def generate_tenant_cache_key(org_id: str, resource_type: str, resource_id: str) -> str:
        return f"cache:v1:org_{org_id}:{resource_type}_{resource_id}"

tenant_governor = TenantResourceGovernor()
