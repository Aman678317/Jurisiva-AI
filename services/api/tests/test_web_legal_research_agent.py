# Comprehensive automated test suite for Web-Based Legal Research Agent & Anti-Hallucination Guardrails

import pytest
from app.case_store import case_store
from app.research_engine import legal_research_engine, OfficialLegalSourceLibrary
from app.main import backend_server

def test_official_source_library_integrity():
    """Verify that all judgments and statutes have official URLs and valid citations."""
    for jdg in OfficialLegalSourceLibrary.OFFICIAL_JUDGMENTS:
        assert jdg["source_type"] == "OFFICIAL_COURT"
        assert jdg["official_url"].startswith("https://")
        assert len(jdg["citation"]) > 4
        assert len(jdg["ratio_decidendi"]) > 10

    for stat in OfficialLegalSourceLibrary.OFFICIAL_STATUTES:
        assert stat["source_type"] == "OFFICIAL_LEGISLATION"
        assert stat["url"].startswith("https://")
        assert len(stat["sections"]) >= 2

def test_search_sources_survey_discrepancies():
    results = OfficialLegalSourceLibrary.search_sources("survey number discrepancy extent deficit", "Karnataka / All India")
    assert len(results) >= 1
    citations = [r["citation"] for r in results]
    assert "2023 INSC 891" in citations # Anandram vs LAO

def test_search_sources_sarfaesi_mortgage():
    results = OfficialLegalSourceLibrary.search_sources("SARFAESI unreleased simple mortgage charge", "All India")
    assert len(results) >= 1
    citations = [r["citation"] for r in results]
    assert any("SARFAESI" in c or "2018 7 SCC 446" in c for c in citations)

def test_anti_hallucination_guarantee_and_verifications():
    case = case_store.get_case("mat_001")
    research_res = legal_research_engine.perform_legal_research(
        case_id="mat_001",
        query="Can mutation entry confer substantive title?",
        jurisdiction="All India",
        date_filter="ALL",
        case_context=case.to_dict()
    )
    assert research_res["anti_hallucination_guarantee"] is not None
    assert research_res["sources_found_count"] >= 1
    for src in research_res["sources"]:
        assert src["verified_status"] == "VERIFIED_OFFICIAL_SOURCE"
        assert src["confidence"] in ["HIGH", "MEDIUM"]

def test_case_context_integration():
    case = case_store.get_case("mat_001")
    research_res = legal_research_engine.perform_legal_research(
        case_id="mat_001",
        query="survey number discrepancy",
        jurisdiction="Karnataka / All India",
        date_filter="ALL",
        case_context=case.to_dict()
    )
    # Check that case document evidence is clearly demarcated from external legal research
    comp = research_res["case_evidence_vs_external_research"]
    assert len(comp["case_document_evidence"]) >= 4
    assert len(comp["external_judicial_authorities"]) >= 2

def test_backend_api_case_research_endpoints():
    # 1. Execute Research
    res = backend_server.handle_request(
        "/api/v1/cases/mat_001/research",
        "POST",
        body={
            "query": "Adverse possession against registered title holder",
            "jurisdiction": "Karnataka / All India",
            "date_filter": "ALL"
        }
    )
    assert res["status"] == "200 OK"
    assert res["data"]["research_id"].startswith("rsch_")
    job_id = res["data"]["research_id"]

    # 2. List Research History
    history_res = backend_server.handle_request("/api/v1/cases/mat_001/research", "GET")
    assert history_res["status"] == "200 OK"
    assert len(history_res["data"]) >= 1

    # 3. Get Single Research Job
    single_res = backend_server.handle_request(f"/api/v1/cases/mat_001/research/{job_id}", "GET")
    assert single_res["status"] == "200 OK"
    assert single_res["data"]["research_id"] == job_id
