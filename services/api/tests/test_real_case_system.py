# Comprehensive automated tests for Real Legal Case System, Dynamic Devolution & OCR Engine

import pytest
from app.case_store import case_store, PropertyCase
from app.ocr_engine import ocr_extraction_engine
from app.main import backend_server

def test_ocr_extraction_engine():
    sample_text = """
    DEED OF ABSOLUTE SALE (ಕ್ರಯ ಪತ್ರ)
    Document No: 9988/2022-23
    VENDOR: Sri. Ramesh Rao S/o Govinda Rao
    PURCHASER: Sri. Suresh Kumar S/o Ananth Kumar
    SCHEDULE: Survey No. 88/2 Hissa 4, Devanahalli
    EXTENT: 3 Acres 18 Guntas
    CONSIDERATION: Rs. 85,00,000/-
    """
    doc_res = ocr_extraction_engine.process_document(sample_text.encode('utf-8'), "Test_Sale_Deed.pdf")
    assert doc_res["processing_status"] == "COMPLETED"
    assert doc_res["extracted_entities"]["vendor"] == "Sri. Ramesh Rao S/o Govinda Rao"
    assert doc_res["extracted_entities"]["purchaser"] == "Sri. Suresh Kumar S/o Ananth Kumar"
    assert doc_res["extracted_entities"]["extent_acres"] == 3
    assert doc_res["extracted_entities"]["extent_guntas"] == 18
    assert doc_res["extracted_entities"]["total_sqft"] == (3 * 43560) + (18 * 1089)

def test_benchmark_case_initialization():
    case = case_store.get_case("mat_001")
    assert case is not None
    assert case.case_id == "mat_001"
    assert case.survey_numbers == "42/1 Hissa 2"
    assert len(case.documents) == 4

def test_dynamic_ownership_chain_generation():
    chain = case_store.get_ownership_chain("mat_001")
    assert chain["chain_status"] == "GENERATED_FROM_EVIDENCE"
    assert len(chain["nodes"]) == 4
    # Node 1
    assert "Venkatappa" in chain["nodes"][0]["holder"]
    assert chain["nodes"][0]["period"] == "1985"
    assert chain["nodes"][0]["source_document"] == "Registered_Sale_Deed_1985.pdf"
    # Node 4 (Current)
    assert "Anand Kumar" in chain["nodes"][3]["holder"]
    assert chain["nodes"][3]["period"] == "2018"
    assert chain["nodes"][3]["source_document"] == "Sale_Deed_2018_Current.pdf"

def test_dynamic_extent_discrepancy_calculation():
    disc = case_store.get_extent_discrepancy("mat_001")
    assert disc["status"] == "DEFICIT_DETECTED"
    assert disc["deficit_guntas"] == 14
    assert disc["deficit_sqft"] == 14 * 1089
    assert disc["parent_extent"] == "2 Acres 24 Guntas"
    assert disc["current_extent"] == "2 Acres 10 Guntas"

def test_dynamic_risk_detection():
    risks = case_store.get_risks("mat_001")
    assert len(risks) >= 2
    severities = [r["severity"] for r in risks]
    assert "CRITICAL" in severities # Unreleased SBI mortgage
    assert "HIGH" in severities     # 14 Guntas deficit

def test_create_new_empty_case_and_empty_states():
    new_case = case_store.create_case({
        "case_name": "Fresh Due Diligence Matter",
        "property_address": "Yelahanka, Bengaluru Urban",
        "survey_numbers": "105/2"
    })
    assert new_case.case_id.startswith("case_")
    
    # Ownership chain on empty case
    chain = case_store.get_ownership_chain(new_case.case_id)
    assert chain["chain_status"] == "NO_DOCUMENTS_UPLOADED"
    assert len(chain["nodes"]) == 0

    # Timeline on empty case
    timeline = case_store.get_timeline(new_case.case_id)
    assert timeline == []

    # Discrepancy on empty case
    disc = case_store.get_extent_discrepancy(new_case.case_id)
    assert disc["status"] == "INSUFFICIENT_DOCUMENTS"

def test_case_api_handlers():
    # 1. List cases
    res = backend_server.handle_request("/api/v1/cases", "GET")
    assert res["status"] == "200 OK"
    assert len(res["data"]) >= 1

    # 2. Get single case
    res = backend_server.handle_request("/api/v1/cases/mat_001", "GET")
    assert res["status"] == "200 OK"
    assert res["data"]["case_id"] == "mat_001"

    # 3. Get ownership
    res = backend_server.handle_request("/api/v1/cases/mat_001/ownership", "GET")
    assert res["status"] == "200 OK"
    assert len(res["data"]["nodes"]) == 4

    # 4. Get extent discrepancy
    res = backend_server.handle_request("/api/v1/cases/mat_001/extent-discrepancy", "GET")
    assert res["status"] == "200 OK"
    assert res["data"]["deficit_guntas"] == 14
