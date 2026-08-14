# Data Intelligence & Knowledge Graph Test Suite

import pytest
from app.data_intelligence.entity_resolver import entity_resolver
from app.data_intelligence.provenance_graph import provenance_graph

def test_dat_001_entity_resolution_exact_match():
    rec_a = {"entity_id": "ent_01", "pan_or_survey": "SURVEY-442/1", "name": "Ramesh Kumar"}
    rec_b = {"entity_id": "ent_02", "pan_or_survey": "SURVEY-442/1", "name": "Ramesh Kumar"}

    match = entity_resolver.resolve_entity_match(rec_a, rec_b)
    assert match["confidence_state"] == "EXACT"
    assert match["requires_human_review"] is False

def test_dat_002_knowledge_graph_edge_locator():
    edge = provenance_graph.add_relationship_edge("org_001", "mat_001", "Party_Ramesh", "OWNS", "Prop_Flat_402", "doc_deed_01", 4)
    assert edge["edge_id"] is not None
    assert edge["evidence"]["document_id"] == "doc_deed_01"
    assert edge["evidence"]["page_number"] == 4

def test_dat_003_knowledge_graph_tenant_isolation():
    provenance_graph.add_relationship_edge("org_tenant_A", "mat_101", "Party_A", "OWNS", "Prop_A", "doc_A", 1)
    provenance_graph.add_relationship_edge("org_tenant_B", "mat_201", "Party_A", "OWNS", "Prop_B", "doc_B", 2)

    tenant_a_results = provenance_graph.query_entity_graph("org_tenant_A", "Party_A")
    assert len(tenant_a_results) == 1
    assert tenant_a_results[0]["org_id"] == "org_tenant_A"
