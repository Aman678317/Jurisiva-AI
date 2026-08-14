# Precedent Citation & Evidence Intelligence Test Suite

import pytest
from app.research.citation_graph import citation_graph_engine
from app.research.evidence_intelligence import evidence_intelligence_engine

def test_rsc_001_add_precedent_edge():
    prov = {"document_id": "sc_order_2024", "page": 4, "paragraph": 12}
    edge = citation_graph_engine.add_precedent_edge("org_001", "Case_A_v_State", "OVERRULES", "Case_B_v_State", prov)
    assert edge.edge_id is not None
    assert edge.relationship == "OVERRULES"
    assert edge.provenance["page"] == 4

def test_rsc_002_zero_cross_tenant_citation():
    citation_graph_engine.add_precedent_edge("org_002", "Case_Unauth", "CITES", "Case_Ref", {"page": 1})

    tenant_a = citation_graph_engine.get_precedent_chain("org_001", "Case_Unauth")
    assert len(tenant_a) == 0

    tenant_b = citation_graph_engine.get_precedent_chain("org_002", "Case_Unauth")
    assert len(tenant_b) == 1

def test_rsc_003_citation_locator_precision():
    invalid_loc = evidence_intelligence_engine.evaluate_citation_precision("Adverse possession claim", {"page": 0}, "Text snippet")
    assert invalid_loc["status"] == "UNVERIFIED"

    valid_loc = evidence_intelligence_engine.evaluate_citation_precision("Adverse possession claim", {"page": 3}, "12 years continuous possession proven.")
    assert valid_loc["status"] == "SUPPORTED"
