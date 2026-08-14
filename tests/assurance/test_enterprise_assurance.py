# Enterprise Assurance & Certification Readiness Test Suite

import pytest
from app.assurance.assurance_verifier import assurance_verifier

def test_asr_001_certification_claims():
    false_claim = assurance_verifier.verify_certification_claim("ISO 27001 Certified Platform", "READINESS_COMPLETE")
    assert false_claim["status"] == "REJECTED"
    assert "prohibited" in false_claim["reason"]

    truthful_claim = assurance_verifier.verify_certification_claim("ISO 27001 Readiness Complete", "READINESS_COMPLETE")
    assert truthful_claim["status"] == "VALIDATED"

def test_asr_002_mock_audit_passes():
    controls = [
        {"id": "CTL-01", "has_evidence": True, "status": "PASS"},
        {"id": "CTL-02", "has_evidence": True, "status": "PASS"},
        {"id": "CTL-03", "has_evidence": True, "status": "PASS"}
    ]
    audit_res = assurance_verifier.run_mock_audit(controls)
    assert audit_res["mock_audit_status"] == "PASS"
    assert audit_res["unproven_controls_count"] == 0

def test_asr_003_mock_audit_fails():
    controls = [
        {"id": "CTL-01", "has_evidence": True, "status": "PASS"},
        {"id": "CTL-02", "has_evidence": False, "status": "UNTESTED"}
    ]
    audit_res = assurance_verifier.run_mock_audit(controls)
    assert audit_res["mock_audit_status"] == "FAIL"
    assert audit_res["unproven_controls_count"] == 1
