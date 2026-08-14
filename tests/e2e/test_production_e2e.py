# End-to-End Production User Journey Test Suite (Journey 1)

import pytest
from app.auth import auth_engine
from app.storage import storage_adapter
from app.jobs import job_engine
from app.search_engine import search_engine
from app.rag_engine import rag_engine
from app.workflows.report_builder import report_builder

def test_e2e_001_complete_advocate_workflow():
    # 1. Authenticate Advocate User
    token_data = auth_engine.create_token("usr_001", "org_001", "LEAD_ADVOCATE")
    assert token_data["access_token"] is not None

    # 2. Document Upload Intent & Validation
    valid, msg = storage_adapter.validate_file_metadata("SaleDeed.pdf", 4839201, "application/pdf")
    assert valid is True

    # 3. Processing Job Creation
    job = job_engine.create_job("org_001", "mat_001", "doc_001")
    assert job["status"] == "QUEUED"

    # 4. Hybrid Search Retrieval (BM25 + pgvector RRF)
    search_res = search_engine.execute_hybrid_search("org_001", "mat_001", "Survey No. 42/1", top_k=5)
    assert len(search_res) > 0

    # 5. RAG Assistant Query & Citation Verification
    rag_res = rag_engine.query_assistant("org_001", "mat_001", "What is the extent of Survey No 42/1?")
    assert rag_res.evidence_status == "SUPPORTED"
    assert len(rag_res.citations) == 1
    assert rag_res.citations[0].status == "VERIFIED_SOURCE"

    # 6. Title Search Report Export
    report = report_builder.generate_report("mat_001", {"survey_number": "42/1"}, [], [])
    assert report["review_status"] == "APPROVED_FOR_EXPORT"
