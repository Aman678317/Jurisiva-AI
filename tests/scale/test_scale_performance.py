# Platform Scale & Performance Engineering Test Suite

import pytest
from app.scale.tenant_governor import TenantResourceGovernor, tenant_governor

def test_scl_001_tenant_concurrency_throttling():
    governor = TenantResourceGovernor(max_concurrent_jobs=2, ttl_sec=600)
    assert governor.acquire_job_slot("org_heavy")["status"] == "ALLOWED"
    assert governor.acquire_job_slot("org_heavy")["status"] == "ALLOWED"

    # 3rd concurrent request from org_heavy is throttled
    throttled = governor.acquire_job_slot("org_heavy")
    assert throttled["status"] == "THROTTLED"
    assert "exceeded max concurrent job capacity" in throttled["reason"]

    # Separate tenant org_light is unimpeded
    assert governor.acquire_job_slot("org_light")["status"] == "ALLOWED"

def test_scl_002_tenant_safe_cache_key():
    key = TenantResourceGovernor.generate_tenant_cache_key("org_001", "matter", "mat_99")
    assert key == "cache:v1:org_org_001:matter_mat_99"
    assert "org_org_001" in key
