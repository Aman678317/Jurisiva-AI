# Enterprise Trust Center & Security Compliance Test Suite

import json
import pytest
from app.trust.trust_center import trust_center

def test_trst_001_public_trust_summary():
    summary = trust_center.get_public_trust_summary()
    assert "Jurisiva AI" in summary["platform_name"]
    assert summary["security_readiness_status"] == "SECURITY_READY"
    assert "SEC-002" in summary["security_controls"]["tenant_isolation"]

def test_trst_002_zero_secret_exposure():
    summary_json = json.dumps(trust_center.get_public_trust_summary())
    assert "SECRET" not in summary_json
    assert "PRIVATE_KEY" not in summary_json
    assert "PASSWORD" not in summary_json

def test_trst_003_subprocessor_registry():
    summary = trust_center.get_public_trust_summary()
    assert len(summary["subprocessors"]) >= 2
    assert summary["subprocessors"][0]["region"] == "ap-south-1 (Mumbai)"
