# Document Processing Pipeline & Indic OCR Evaluation Test Suite

import pytest
from workers.ingestion_worker.ocr_engine import ocr_gateway
from workers.ingestion_worker.pipeline import document_pipeline, PDFTextDetector, EntityCandidateExtractor

def test_doc_001_pdf_text_vs_scanned_detection():
    assert PDFTextDetector.inspect_page(10) is True   # Low text density -> Scanned OCR required
    assert PDFTextDetector.inspect_page(500) is False # Native text embedded PDF

def test_doc_002_indic_ocr_gateway():
    res = ocr_gateway.process_page_image(1, True)
    assert "Survey No. 42/1" in res["raw_text"]
    assert "mr" in res["detected_languages"]
    assert res["quality_score"] >= 0.90
    assert len(res["layout_blocks"]) == 3
    assert res["words"][0]["bbox"] is not None

def test_doc_003_entity_candidate_extraction():
    sample_text = "Deed executed on 14-08-1985 for Survey No. 42/1 Hissa 2 measuring 2 Acres 24 Guntas"
    candidates = EntityCandidateExtractor.extract_candidates(sample_text, 1)
    assert len(candidates) >= 3

    sy_candidate = next((c for c in candidates if c["entity_type"] == "SURVEY_NUMBER"), None)
    assert sy_candidate is not None
    assert sy_candidate["normalized_value"] == "42/1"

    extent_candidate = next((c for c in candidates if c["entity_type"] == "EXTENT"), None)
    assert extent_candidate is not None
    assert "2 Acres 24 Guntas" in extent_candidate["normalized_value"]

def test_doc_004_e2e_pipeline_execution():
    result = document_pipeline.process_document("doc_test_101", "SaleDeed.pdf", True)
    assert result["status"] == "READY"
    assert len(result["pipeline_log"]) == 5
    assert len(result["entities"]) > 0
    assert result["raw_ocr_text"] == result["normalized_text"]

def test_doc_005_idempotency_retry_safety():
    run1 = document_pipeline.process_document("doc_test_101", "SaleDeed.pdf", True)
    run2 = document_pipeline.process_document("doc_test_101", "SaleDeed.pdf", True)
    assert run1["document_id"] == run2["document_id"]
    assert run1["quality_score"] == run2["quality_score"]
