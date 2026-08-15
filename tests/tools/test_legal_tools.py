# Unit & Integration Tests for Legal AI Tools Suite

import pytest
from app.tools import (
    legal_research_tool,
    contract_review_tool,
    summarization_tool,
    citation_lookup_tool,
    document_comparison_tool,
    case_timeline_tool,
    batch_ingestion_engine,
    property_paper_scanner_tool,
    voice_assistant_tool,
    property_case_dossier_engine,
    review_table_matrix_engine
)
from app.main import backend_server

def test_legal_research_tool():
    results = legal_research_tool.search_precedents("adverse possession limitation")
    assert len(results) > 0
    assert "2024 INSC 412" in results[0]["citation"]
    assert results[0]["authority_level"] == "Level 1 (Apex Court — Binding on all Courts in India under Article 141)"

def test_citation_graph_tool():
    graph_res = legal_research_tool.generate_citation_graph("property title and mortgages")
    assert graph_res["total_nodes"] >= 6
    assert graph_res["total_edges"] >= 4
    assert any(n["id"] == "node_sc_412" for n in graph_res["graph_data"]["nodes"])
    assert "matter_relevance_summary" in graph_res

def test_review_tables_matrix_and_customer_ask():
    matrix = review_table_matrix_engine.get_full_matrix()
    assert len(matrix) == 4
    assert matrix[0]["document"] == "Sale Deed #1985"
    assert matrix[2]["status"] == "UNRELEASED MORTGAGE"
    assert matrix[3]["status"] == "EXTENT MISMATCH (-14 Guntas)"

    answer = review_table_matrix_engine.answer_customer_ask("What about customer asking if tax receipts are attached?")
    assert "tax clearance" in answer["answer"].lower() or "receipt" in answer["answer"].lower()
    assert len(answer["evidence_rows"]) >= 1

def test_contract_review_tool():
    text = "The vendor shall indemnify the buyer against all liabilities without limitation. Governing law shall be India."
    report = contract_review_tool.review_contract(text, "Vendor_Master_Agreement.docx")
    assert report["overall_risk"] == "HIGH"
    assert report["total_clauses_reviewed"] >= 2
    assert any(c["clause_type"] == "INDEMNITY" for c in report["findings"])

def test_summarization_tool():
    summary = summarization_tool.summarize_document("Sale deed deed text", "Deed_1985.pdf")
    assert "42/1 Hissa 2" in summary["property_particulars"]["survey_number"]
    assert len(summary["key_parties"]) == 2
    assert len(summary["covenants_and_warranties"]) >= 2

def test_citation_lookup_tool():
    cite_info = citation_lookup_tool.lookup_citation("2024 INSC 412")
    assert cite_info["status"] == "VALID_VERIFIED_CITATION"
    assert cite_info["case_details"]["court"] == "Supreme Court of India"

def test_document_comparison_tool():
    diff = document_comparison_tool.compare_documents("SaleDeed_1985.pdf", "SaleDeed_2018.pdf")
    assert "Material Discrepancy" in diff["comparison_summary"]
    assert any(d["field"] == "Schedule Property Extent" for d in diff["clause_diffs"])

def test_case_timeline_tool():
    timeline = case_timeline_tool.get_timeline("mat_001")
    assert timeline["total_events"] == 4
    assert timeline["events"][0]["date"] == "1985-08-14"
    assert timeline["events"][2]["status"] == "UNRELEASED_ALERT"

def test_batch_ingestion_engine():
    files = [
        {"filename": "Doc1.pdf", "size": 50000, "mime_type": "application/pdf"},
        {"filename": "Deed2.docx", "size": 120000, "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"},
        {"filename": "Scan.jpg", "size": 300000, "mime_type": "image/jpeg"}
    ]
    batch_res = batch_ingestion_engine.process_batch(files)
    assert batch_res["total_files"] == 3
    assert batch_res["successful_ingestions"] == 3
    assert batch_res["processed_documents"][2]["is_scanned"] is True

def test_document_upload_endpoint():
    res_upload = backend_server.handle_request(
        "/api/v1/documents/upload",
        "POST",
        body={
            "filename": "Partition_Deed_2015.pdf",
            "byte_size": 240000,
            "mime_type": "application/pdf",
            "matter_id": "mat_001"
        }
    )
    assert res_upload["status"] == "201 Created"
    assert res_upload["data"]["filename"] == "Partition_Deed_2015.pdf"
    assert res_upload["data"]["status"] == "READY"
    assert res_upload["data"]["chunks_indexed"] >= 2

def test_property_paper_scanner_tool():
    scan_res_1985 = property_paper_scanner_tool.scan_property_paper("Registered_Sale_Deed_1985.pdf")
    assert "1234/1985" in scan_res_1985["registration_details"]["deed_number"]
    assert "42/1 Hissa 2" in scan_res_1985["property_particulars"]["survey_number"]
    assert scan_res_1985["property_particulars"]["total_extent"] == "2 Acres 24 Guntas (104,544 Sq.Ft)"
    assert scan_res_1985["ocr_intelligence"]["ocr_confidence_score"] >= 0.95

    scan_res_mutation = property_paper_scanner_tool.scan_property_paper("Mutation_Extract_1986.pdf")
    assert "M.R. No. 14/1986" in scan_res_mutation["registration_details"]["deed_number"]
    assert scan_res_mutation["title_risk_analysis"]["title_chain_status"] == "KHATA SANCTIONED"

    scan_res_mortgage = property_paper_scanner_tool.scan_property_paper("Mortgage_Deed_2010.pdf")
    assert "50,00,000" in scan_res_mortgage["financial_valuation"]["total_consideration_inr"]
    assert scan_res_mortgage["title_risk_analysis"]["risk_rating"] == "CRITICAL_RISK"

def test_voice_assistant_tool():
    voice_res = voice_assistant_tool.explain_simply("extent mismatch", "en")
    assert "easy_explanation_text" in voice_res
    assert "14 Guntas" in voice_res["easy_explanation_text"]
    assert "hindi_summary" in voice_res
    assert len(voice_res["key_takeaways"]) == 3

def test_property_case_dossier_engine():
    dossier = property_case_dossier_engine.generate_full_dossier("mat_001")
    assert dossier["workflow_status"] == "COMPLETED"
    assert len(dossier["steps_executed"]) == 10
    assert "final_report" in dossier
    assert "facts" in dossier["final_report"]
    assert len(dossier["final_report"]["missing_documents"]) >= 4

def test_backend_tool_endpoints():
    res_research = backend_server.handle_request("/api/v1/research/search", "POST", body={"query": "adverse possession"})
    assert res_research["status"] == "200 OK"

    res_graph = backend_server.handle_request("/api/v1/research/graph", "POST", body={"topic": "title"})
    assert res_graph["status"] == "200 OK"
    assert "graph_data" in res_graph["data"]

    res_review_ask = backend_server.handle_request("/api/v1/review-tables/ask", "POST", body={"question": "What about tax receipts?"})
    assert res_review_ask["status"] == "200 OK"
    assert "tax" in res_review_ask["data"]["answer"].lower() or "receipt" in res_review_ask["data"]["answer"].lower()

    res_contract = backend_server.handle_request("/api/v1/contracts/review", "POST", body={"text": "indemnify and hold harmless"})
    assert res_contract["status"] == "200 OK"

    res_timeline = backend_server.handle_request("/api/v1/timeline/mat_001", "GET")
    assert res_timeline["status"] == "200 OK"

    res_scanner = backend_server.handle_request("/api/v1/scanner/read-paper", "POST", body={"document_name": "SaleDeed_1985.pdf"})
    assert res_scanner["status"] == "200 OK"

    res_voice = backend_server.handle_request("/api/v1/voice/explain", "POST", body={"query": "explain risks", "language": "hi"})
    assert res_voice["status"] == "200 OK"
    assert "hindi_summary" in res_voice["data"]

    res_workflow = backend_server.handle_request("/api/v1/cases/run-full-workflow", "POST", body={"matter_id": "mat_001"})
    assert res_workflow["status"] == "200 OK"
    assert res_workflow["data"]["workflow_status"] == "COMPLETED"

    res_report = backend_server.handle_request("/api/v1/cases/mat_001/report", "GET")
    assert res_report["status"] == "200 OK"
    assert "facts" in res_report["data"]
