# Comprehensive automated tests for Legal Drafting Studio, AI Correction Engine, and Document Scanner

import pytest
from app.case_store import case_store
from app.drafting_engine import drafting_engine
from app.correction_engine import correction_engine
from app.ocr_engine import ocr_extraction_engine
from app.main import backend_server

def test_court_petition_generation_and_grounding():
    case = case_store.get_case("mat_001")
    assert case is not None

    draft = drafting_engine.generate_draft(case.to_dict(), "COURT_PETITION")
    assert draft["draft_category"] == "Court Petition"
    assert "PETITION UNDER SECTION 106 & 136(2)" in draft["title"]
    assert "BEFORE THE COURT OF THE ASSISTANT COMMISSIONER" in draft["content"]
    assert "14 Guntas" in draft["content"]
    assert "2023 INSC 891" in draft["content"] # Apex court citation
    assert len(draft["evidence_citations"]) >= 4

def test_legal_notice_generation():
    case = case_store.get_case("mat_001")
    draft = drafting_engine.generate_draft(case.to_dict(), "LEGAL_NOTICE")
    assert draft["draft_category"] == "Legal Notice"
    assert "DEMAND FOR EXECUTION AND REGISTRATION OF DEED OF DISCHARGE" in draft["title"]
    assert "State Bank of India" in draft["content"]
    assert "Rs. 50,00,000/-" in draft["content"]

def test_revenue_application_generation():
    case = case_store.get_case("mat_001")
    draft = drafting_engine.generate_draft(case.to_dict(), "REVENUE_APPLICATION")
    assert draft["draft_category"] == "Revenue Application"
    assert "MOJINI 11E SURVEY SKETCH" in draft["title"]
    assert "TAHSILDAR & ASSISTANT DIRECTOR OF LAND RECORDS" in draft["content"]

def test_ai_draft_quality_review():
    case = case_store.get_case("mat_001")
    draft = drafting_engine.generate_draft(case.to_dict(), "COURT_PETITION")
    review = drafting_engine.review_draft(draft["draft_id"], case.to_dict())
    assert review["readiness_status"] == "READY"
    assert review["quality_score"] == "98%"
    assert review["checklist"]["statutory_grounds_specified"] is True
    assert review["checklist"]["prayer_and_relief_formulated"] is True

def test_ai_draft_copilot_refinement_and_versioning():
    case = case_store.get_case("mat_001")
    draft = drafting_engine.generate_draft(case.to_dict(), "COURT_PETITION")
    draft_id = draft["draft_id"]

    # Refine formal tone
    refined = drafting_engine.refine_draft_copilot(draft_id, "Make tone more formal for High Court")
    assert "most respectfully and solemnly submits" in refined["content"]
    
    # Check version history ledger
    versions = drafting_engine.get_versions(draft_id)
    assert len(versions) == 2
    assert versions[0]["version_num"] == "v1"
    assert versions[1]["version_num"] == "v2"

def test_ai_document_correction_engine():
    case = case_store.get_case("mat_001")
    doc = case.documents[0] # 1985 deed
    corrections = correction_engine.check_document_corrections(doc)
    assert len(corrections) >= 1
    assert corrections[0]["original_text"] == "Survey No 421 Hissa 2"
    assert corrections[0]["ai_suggestion"] == "Survey No. 42/1 Hissa 2"

def test_correction_action_and_immutable_audit_trail():
    case_id = "mat_001"
    res = correction_engine.apply_action(
        case_id=case_id,
        doc_id="doc_001",
        correction_id="corr_01",
        action="ACCEPT",
        user_name="Adv. Rajesh Sharma"
    )
    assert res["status"] == "SUCCESS"
    assert res["audit_entry"]["action"] == "ACCEPT"

    audit_trail = correction_engine.get_audit_trail(case_id)
    assert len(audit_trail) >= 1
    assert audit_trail[-1]["applied_by"] == "Adv. Rajesh Sharma"

def test_22_field_document_review():
    case = case_store.get_case("mat_001")
    doc_2018 = case.documents[3] # 2018 deed
    review = ocr_extraction_engine.review_document(doc_2018)
    assert "Extent Shortfall of 14 Guntas" in [e["issue"] for e in review["potential_errors"]]
    assert "Mojini 11E Tatkal Phodi Survey Sketch" in [m["item"] for m in review["missing_information"]]
    assert len(review["recommended_next_steps"]) >= 3

def test_backend_api_endpoints_for_drafting():
    # 1. Generate Draft
    res = backend_server.handle_request(
        "/api/v1/cases/mat_001/drafts",
        "POST",
        body={"draft_type": "COURT_PETITION"}
    )
    assert res["status"] == "201 Created"
    draft_id = res["data"]["draft_id"]

    # 2. Review Draft
    res = backend_server.handle_request(
        f"/api/v1/cases/mat_001/drafts/{draft_id}/review",
        "POST"
    )
    assert res["status"] == "200 OK"
    assert res["data"]["readiness_status"] == "READY"

    # 3. AI Refine Draft
    res = backend_server.handle_request(
        f"/api/v1/cases/mat_001/drafts/{draft_id}/ai-refine",
        "POST",
        body={"instruction": "Add Section 106 grounds"}
    )
    assert res["status"] == "200 OK"
    assert "Section 106" in res["data"]["content"]

    # 4. Check Corrections
    res = backend_server.handle_request(
        "/api/v1/cases/mat_001/documents/doc_001/check-corrections",
        "POST"
    )
    assert res["status"] == "200 OK"
    assert len(res["data"]) >= 1
