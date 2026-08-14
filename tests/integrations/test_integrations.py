# External Data Sources & India Integration Test Suite

import pytest
from app.integrations.registry import source_registry
from app.integrations.mock_adapters import mock_court_adapter, mock_property_adapter
from app.integrations.orchestrator import research_orchestrator, SSRFSecurityGuard

def test_ind_001_source_registry_authority_level():
    ecourts_src = source_registry.get_source("src_ecourts")
    assert ecourts_src is not None
    assert ecourts_src.authority_level == "LEVEL_1"
    assert ecourts_src.is_official is True

def test_ind_002_mock_court_adapter_search_normalize():
    results = mock_court_adapter.search("104/2019", {})
    assert len(results) == 1
    assert results[0].case_number == "O.S. No. 104/2019"

    record = mock_court_adapter.fetch(results[0].case_id)
    normalized = mock_court_adapter.normalize(record)
    assert normalized.canonical_type == "COURT_ORDER"
    assert normalized.provenance["content_hash"] is not None

def test_ind_003_mock_property_adapter():
    parcels = mock_property_adapter.search("42/1", {})
    assert len(parcels) == 1
    assert parcels[0].survey_number == "42/1"
    assert "Krishnappa" in parcels[0].owner_name

    health = mock_property_adapter.health_check()
    assert health["status"] == "HEALTHY"

def test_ind_004_ssrf_url_security_guard():
    assert SSRFSecurityGuard.validate_external_url("http://localhost:8000") is False
    assert SSRFSecurityGuard.validate_external_url("http://127.0.0.1/admin") is False
    assert SSRFSecurityGuard.validate_external_url("http://169.254.169.254/latest/meta-data") is False
    assert SSRFSecurityGuard.validate_external_url("https://ecourts.gov.in/services") is True

def test_ind_005_research_orchestrator():
    court_res = research_orchestrator.execute_court_research("org_001", "mat_001", "104/2019")
    assert court_res["status"] == "SUCCESS"
    assert court_res["verification_status"] == "SOURCE_RETRIEVED"
    assert court_res["authority_level"] == "LEVEL_1"

    unauthorized_res = research_orchestrator.execute_court_research("", "mat_001", "104/2019")
    assert unauthorized_res["status"] == "FORBIDDEN"
