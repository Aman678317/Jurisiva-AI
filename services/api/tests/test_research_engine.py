# Unit & Integration Tests for Jurisiva AI Research Engine

import pytest
import os
import sys

# Add services/api to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.research.planner import research_planner
from app.research.retrieval import document_retriever
from app.research.evidence import evidence_extractor
from app.research.web_research import web_researcher
from app.research.source_validator import source_validator
from app.research.analyzer import research_analyst
from app.research.citations import citation_builder
from app.research.synthesizer import research_synthesizer
from app.research.orchestrator import research_orchestrator
from app.main import backend_server

def test_research_planner():
    # Test intent parsing and jurisdiction scoping
    plan = research_planner.plan_research("Who is the current owner of Survey No 42/1?")
    assert plan.mode == "OWNERSHIP_RESEARCH"
    assert plan.intent == "OWNERSHIP_VERIFICATION"
    assert plan.jurisdiction["state"] == "Karnataka"
    assert len(plan.sub_tasks) > 0

    legal_plan = research_planner.plan_research("Find relevant laws and Supreme Court judgments on extent mismatch")
    assert legal_plan.mode == "LEGAL_RESEARCH"
    assert "external_research" in legal_plan.required_tools

def test_document_retrieval():
    chunks = document_retriever.retrieve_chunks("org_001", "mat_001", "Survey No 42/1 extent", top_k=4)
    assert len(chunks) > 0
    assert any("42/1" in c["text"] for c in chunks)
    assert any(c["page_number"] >= 1 for c in chunks)

def test_evidence_extraction():
    chunks = document_retriever.retrieve_chunks("org_001", "mat_001", "Survey No 42/1 extent", top_k=4)
    evidence = evidence_extractor.extract_evidence(chunks, "extent and survey number")
    assert len(evidence) > 0
    
    # Check that each evidence snippet has page number and exact quote
    for ev in evidence:
        assert ev.page_number >= 1
        assert len(ev.exact_quote) > 0
        assert ev.confidence >= 0.90

def test_web_research_and_source_validation():
    external_sources = web_researcher.search_external_legal_sources("extent mismatch akarband durasti", max_sources=3)
    assert len(external_sources) > 0
    
    validated = source_validator.validate_sources(external_sources, {"state": "Karnataka"})
    assert len(validated) > 0
    assert validated[0]["validation_status"] in ["VERIFIED_AUTHORITATIVE", "PROVISIONAL_EXTERNAL"]
    assert validated[0]["authority_level"] in ["LEVEL_1_APEX", "LEVEL_2_HIGH_COURT", "GOVERNMENT_REGISTRY"]

def test_analyzer_ownership_and_risks():
    chunks = document_retriever.retrieve_chunks("org_001", "mat_001", "ownership mortgage extent", top_k=6)
    ownership = research_analyst.build_ownership_chain(chunks)
    assert ownership["current_owner"] == "Sri. Anand Kumar"
    assert len(ownership["nodes"]) >= 3

    risks = research_analyst.detect_conflicts_and_risks(chunks)
    assert len(risks) >= 3
    # Check that critical encumbrance and high extent deficit are detected
    categories = [r.category for r in risks]
    severities = [r.severity for r in risks]
    assert "Encumbrance Risk" in categories
    assert "CRITICAL" in severities
    assert "HIGH" in severities

def test_citation_builder():
    chunks = document_retriever.retrieve_chunks("org_001", "mat_001", "Sale Deed", top_k=3)
    evidence = evidence_extractor.extract_evidence(chunks, "Sale Deed")
    doc_cites = citation_builder.build_document_citations(evidence)
    assert len(doc_cites) > 0
    assert doc_cites[0]["type"] == "DOCUMENT_EVIDENCE"
    assert doc_cites[0]["verification_status"] == "VERIFIED_PRIMARY_SOURCE"

def test_synthesizer():
    plan = research_planner.plan_research("Who is the current owner?")
    chunks = document_retriever.retrieve_chunks("org_001", "mat_001", "owner", top_k=4)
    evidence = evidence_extractor.extract_evidence(chunks, "owner")
    ownership = research_analyst.build_ownership_chain(chunks)
    risks = research_analyst.detect_conflicts_and_risks(chunks)
    ext_sources = web_researcher.search_external_legal_sources("property title")
    doc_cites = citation_builder.build_document_citations(evidence)
    ext_cites = citation_builder.build_external_citations(ext_sources)

    synth = research_synthesizer.synthesize(
        query="Who is the current owner?",
        plan=plan,
        evidence=evidence,
        risks=risks,
        ownership=ownership,
        external_sources=ext_sources,
        doc_citations=doc_cites,
        ext_citations=ext_cites
    )

    assert "Anand Kumar" in synth["executive_summary"]
    assert len(synth["key_findings"]) > 0
    assert len(synth["recommendations"]) > 0
    assert "Based strictly on uploaded documents" in synth["legal_safety_disclaimer"]

def test_orchestrator_sync_and_async():
    # Test sync execution
    res = research_orchestrator.execute_research_sync("Is there any survey number or extent mismatch?")
    assert res["status"] == "COMPLETED"
    assert res["progress_percentage"] == 100
    assert len(res["live_steps"]) >= 6
    assert "result" in res
    assert len(res["result"]["risk_findings"]) > 0

    # Test report generation
    report = research_orchestrator.generate_full_diligence_report("mat_001")
    assert report["report_title"] == "CONFIDENTIAL PROPERTY TITLE DUE DILIGENCE REPORT"
    assert "deficit" in report["property_details"]

def test_api_endpoints():
    # Test POST /api/v1/research
    res = backend_server.handle_request(
        endpoint="/api/v1/research",
        method="POST",
        body={"query": "Who is the current owner?", "mode": "OWNERSHIP_RESEARCH", "matter_id": "mat_001"}
    )
    assert res["status"] == "200 OK"
    data = res["data"]
    assert data["status"] == "COMPLETED"
    assert "executive_summary" in data["result"]

    # Test GET /api/v1/cases/mat_001/report
    report_res = backend_server.handle_request(
        endpoint="/api/v1/cases/mat_001/report",
        method="GET"
    )
    assert report_res["status"] == "200 OK"
    assert "report_title" in report_res["data"]
