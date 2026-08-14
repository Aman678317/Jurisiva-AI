# Institutional Governance & Risk Compliance Test Suite

import pytest
from app.governance.compliance_verifier import compliance_verifier

def test_gov_001_open_source_license_verification_pass():
    pkgs = [
        {"name": "fastapi", "license": "MIT"},
        {"name": "pydantic", "license": "MIT"},
        {"name": "sqlalchemy", "license": "MIT"}
    ]
    res = compliance_verifier.verify_license_compliance(pkgs)
    assert res["status"] == "PASS"
    assert res["violations_count"] == 0

def test_gov_002_prohibited_copyleft_license_flagged():
    pkgs = [{"name": "gpl_tool", "license": "GPL-3.0"}]
    res = compliance_verifier.verify_license_compliance(pkgs)
    assert res["status"] == "FAIL"
    assert res["violations_count"] == 1

def test_gov_003_ai_action_approval_levels():
    high_no_approval = compliance_verifier.verify_ai_action_approval("HIGH", False)
    assert high_no_approval["status"] == "BLOCKED"

    high_approved = compliance_verifier.verify_ai_action_approval("HIGH", True)
    assert high_approved["status"] == "APPROVED"

    critical_action = compliance_verifier.verify_ai_action_approval("CRITICAL", True)
    assert critical_action["status"] == "REJECTED"
