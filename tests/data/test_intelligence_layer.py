# Data Platform & Governed Intelligence Test Suite

import pytest
from app.intelligence.evidence_graph import evidence_graph_engine
from app.intelligence.claim_verifier import claim_verifier

def test_dat_001_add_evidence_graph_edge():
    prov = {"document_id": "doc_1985", "page_number": 1, "extraction_method": "INDIC_OCR"}
    edge = evidence_graph_engine.add_evidence_edge("org_001", "person_venkatappa", "TRANSFERRED_TITLE_TO", "person_krishnappa", prov)
    assert edge["edge_id"] is not None
    assert edge["provenance"]["document_id"] == "doc_1985"

def test_dat_002_zero_cross_tenant_graph_traversal():
    evidence_graph_engine.add_evidence_edge("org_002", "person_unauthorized", "OWNS", "parcel_999", {"source": "test"})

    tenant_a_edges = evidence_graph_engine.query_tenant_graph("org_001", "person_unauthorized")
    assert len(tenant_a_edges) == 0

    tenant_b_edges = evidence_graph_engine.query_tenant_graph("org_002", "person_unauthorized")
    assert len(tenant_b_edges) == 1

def test_dat_003_claim_verifier_classification():
    unverified = claim_verifier.verify_claim("Venkatappa owns Survey 999", [])
    assert unverified["status"] == "UNVERIFIED"

    contradicted = claim_verifier.verify_claim("Venkatappa owns 5 Acres", [{"status": "POSSIBLE_CONFLICT"}])
    assert contradicted["status"] == "CONTRADICTED"
