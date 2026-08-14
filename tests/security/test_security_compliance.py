# Security, Privacy & AI Governance Test Suite

import pytest
from app.security.model_registry import model_registry
from app.security.disaster_recovery import dr_simulator
from app.security.red_team import red_team_verifier
from app.integrations.orchestrator import SSRFSecurityGuard

def test_sec_001_model_registry_approval():
    assert model_registry.is_model_approved("gpt-4o-mini", "PROPERTY_DUE_DILIGENCE") is True
    assert model_registry.is_model_approved("unapproved-model-v99") is False
    assert model_registry.is_model_approved("gpt-4o-mini", "UNAPPROVED_WORKFLOW") is False

def test_sec_002_red_team_tenant_isolation():
    audit_res = red_team_verifier.verify_tenant_isolation("org_001", "org_002")
    assert audit_res["status"] == "PASS"
    assert audit_res["auth_guard_blocked"] is True
    assert audit_res["search_engine_blocked"] is True
    assert audit_res["unauthorized_records_leaked"] == 0

def test_sec_003_ssrf_security_guard():
    assert SSRFSecurityGuard.validate_external_url("http://127.0.0.1:5432") is False
    assert SSRFSecurityGuard.validate_external_url("http://localhost:9000") is False
    assert SSRFSecurityGuard.validate_external_url("http://169.254.169.254/latest/meta-data") is False
    assert SSRFSecurityGuard.validate_external_url("https://ecourts.gov.in/services") is True

def test_sec_004_disaster_recovery_drill():
    dr_res = dr_simulator.run_restore_test("snap_2026_08_14")
    assert dr_res["status"] == "PASS"
    assert dr_res["database_restored"] is True
    assert dr_res["storage_restored"] is True
    assert dr_res["tenant_integrity_passed"] is True
    assert dr_res["measured_rto_seconds"] < 10.0
