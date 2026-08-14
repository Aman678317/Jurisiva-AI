# Hybrid Search, RAG & Citation Validation Test Suite

import pytest
from app.chunking import chunker
from app.embeddings import embedding_provider, vector_index
from app.search_engine import search_engine
from app.rag_engine import rag_engine, EvidenceSufficiencyGate, CitationValidator

@pytest.fixture(autouse=True)
def setup_search_fixtures():
    test_pages = [
        {"page_number": 1, "raw_ocr_text": "REGISTERED NO: 1234/1985\n\nTHIS DEED OF SALE executed on 14-08-1985."},
        {"page_number": 3, "raw_ocr_text": "SCHEDULE PROPERTY: Survey No. 42/1 Hissa 2, Extent: 2 Acres 24 Guntas (104,544 Sq.Ft), Devanahalli."}
    ]
    chunks = chunker.chunk_document("org_001", "mat_001", "doc_001", "v1", test_pages)
    vector_index.upsert_chunks(chunks)

def test_rag_001_structure_aware_chunking():
    test_pages = [
        {"page_number": 1, "raw_ocr_text": "REGISTERED NO: 1234/1985\n\nTHIS DEED OF SALE executed on 14-08-1985."},
        {"page_number": 3, "raw_ocr_text": "SCHEDULE PROPERTY: Survey No. 42/1 Hissa 2, Extent: 2 Acres 24 Guntas (104,544 Sq.Ft), Devanahalli."}
    ]
    chunks = chunker.chunk_document("org_001", "mat_001", "doc_001", "v1", test_pages)
    assert len(chunks) == 2
    assert chunks[0].content_hash is not None
    assert chunks[1].page_number == 3

def test_rag_002_exact_identifier_overboost():
    results = search_engine.execute_hybrid_search("org_001", "mat_001", "Survey No. 42/1", top_k=5)
    assert len(results) > 0
    assert "Survey No. 42/1" in results[0].text
    assert results[0].page_number == 3

def test_rag_003_cross_tenant_search_block():
    cross_tenant_results = search_engine.execute_hybrid_search("org_002", "mat_001", "Survey No. 42/1", top_k=5)
    assert len(cross_tenant_results) == 0

def test_rag_004_evidence_sufficiency_gate():
    status, sufficient = EvidenceSufficiencyGate.evaluate_sufficiency([], "Non-existent query text")
    assert status == "INSUFFICIENT_EVIDENCE"
    assert sufficient is False

    rag_res = rag_engine.query_assistant("org_001", "mat_001", "Where is the secret nuclear code?")
    assert rag_res["evidence_status"] == "INSUFFICIENT_EVIDENCE"
    assert "Insufficient evidence" in rag_res["answer"]

def test_rag_005_grounded_answer_and_citation():
    rag_res = rag_engine.query_assistant("org_001", "mat_001", "What is the extent of Survey No 42/1?")
    assert rag_res["evidence_status"] == "SUPPORTED"
    assert len(rag_res["citations"]) == 1
    assert rag_res["citations"][0]["status"] == "VERIFIED_SOURCE"
    assert rag_res["citations"][0]["page_number"] == 3

def test_rag_006_citation_validator_catches_invalid_page():
    invalid_citation = [{"document_id": "doc_001", "page_number": 99, "excerpt": "Fake text"}]
    valid_chunks = [{"page_number": 3, "text": "Real text"}]
    validated = CitationValidator.validate_citations(invalid_citation, valid_chunks)
    assert validated[0]["status"] == "UNVERIFIED_CITATION"
