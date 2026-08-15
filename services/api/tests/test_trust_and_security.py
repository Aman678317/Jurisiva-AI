# Comprehensive automated tests for Jurisiva AI Trust & Security Center & Audit Engine

import pytest
from app.security.security_config import SECURITY_POSTURE
from app.security.provider_registry import provider_registry
from app.security.audit_service import security_audit_service
from app.main import backend_server

def test_security_status_and_zero_fake_claims():
    """Verify that all compliance statuses are strictly truthful and never claim fake certifications."""
    res = backend_server.handle_request("/api/v1/security/status", "GET")
    assert res["status"] == "200 OK"
    data = res["data"]

    assert data["organization"] == "Jurisiva AI Technologies Private Limited"
    assert "Evidence-first AI" in data["positioning"]

    # Verify trust indicators
    indicators = data["trust_indicators"]
    assert len(indicators) >= 5
    ind_names = [i["name"] for i in indicators]
    assert "Encryption at Rest" in ind_names
    assert "Encryption in Transit" in ind_names
    assert "Tenant Isolation" in ind_names

    # Verify truthful compliance framework statuses
    compliance = data["compliance_status"]
    comp_map = {c["framework"]: c["status"] for c in compliance}

    # DPDP and IT Act are verified implemented
    assert comp_map.get("Digital Personal Data Protection Act, 2023 (DPDP)") == "VERIFIED"
    assert comp_map.get("Information Technology Act, 2000 & SPDI Rules") == "VERIFIED"

    # SOC 2 and ISO 27001 are strictly IN PROGRESS - NOT falsely claimed as certified
    assert comp_map.get("SOC 2 Type II (Security, Confidentiality & Availability)") == "IN PROGRESS"
    assert comp_map.get("ISO/IEC 27001:2022 (Information Security Management)") == "IN PROGRESS"

def test_subprocessor_registry_integrity():
    """Verify that subprocessors are loaded from the configuration and declare data residency."""
    res = backend_server.handle_request("/api/v1/security/providers", "GET")
    assert res["status"] == "200 OK"
    providers = res["data"]
    assert len(providers) >= 4

    p_names = [p["provider"] for p in providers]
    assert any("AWS" in p for p in p_names)
    assert any("Google" in p for p in p_names)
    assert any("Bhoomi" in p for p in p_names)

    for p in providers:
        assert p["status"] == "VERIFIED & ACTIVE"
        assert len(p["region"]) > 0

def test_security_documents_list():
    res = backend_server.handle_request("/api/v1/security/documents", "GET")
    assert res["status"] == "200 OK"
    docs = res["data"]
    assert len(docs) >= 4
    titles = [d["title"] for d in docs]
    assert "Enterprise Security Whitepaper" in titles
    assert "Data Processing Agreement (DPA)" in titles
    assert "AI Ethics, Governance & Model Safety Policy" in titles

def test_immutable_audit_log_recording_and_retrieval():
    # 1. Fetch current audit logs
    res = backend_server.handle_request("/api/v1/security/audit-log", "GET")
    assert res["status"] == "200 OK"
    initial_count = len(res["data"])
    assert initial_count >= 1

    # 2. Trigger an update in security settings
    patch_res = backend_server.handle_request(
        "/api/v1/security/settings",
        "PATCH",
        body={"data_retention_days": 60}
    )
    assert patch_res["status"] == "200 OK"
    assert patch_res["data"]["data_retention_days"] == 60

    # 3. Verify that the update created an immutable audit event
    res_after = backend_server.handle_request("/api/v1/security/audit-log", "GET")
    assert len(res_after["data"]) == initial_count + 1
    last_event = res_after["data"][-1]
    assert last_event["action"] == "SECURITY_SETTINGS_UPDATED"
    assert last_event["resource_type"] == "SecurityPolicy"
