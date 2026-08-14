# Data Intelligence & Knowledge Graph Test Suite

from app.data_intelligence.entity_resolver import entity_resolver
from app.data_intelligence.provenance_graph import provenance_graph

describe("Chapter 27 Data Intelligence, Analytics & Knowledge Graph", () => {
  test("DAT-001: Entity resolution correctly tags EXACT match for identical Survey Numbers", () => {
    const recA = { entity_id: "ent_01", pan_or_survey: "SURVEY-442/1", name: "Ramesh Kumar" };
    const recB = { entity_id: "ent_02", pan_or_survey: "SURVEY-442/1", name: "Ramesh Kumar" };

    const match = entity_resolver.resolve_entity_match(recA, recB);
    expect(match.confidence_state).toBe("EXACT");
    expect(match.requires_human_review).toBe(false);
  });

  test("DAT-002: Knowledge graph edge stores non-zero page evidence locator", () => {
    const edge = provenance_graph.add_relationship_edge("org_001", "mat_001", "Party_Ramesh", "OWNS", "Prop_Flat_402", "doc_deed_01", 4);
    expect(edge.edge_id).toBeDefined();
    expect(edge.evidence.document_id).toBe("doc_deed_01");
    expect(edge.evidence.page_number).toBe(4);
  });

  test("DAT-003: Knowledge graph query enforces tenant isolation", () => {
    provenance_graph.add_relationship_edge("org_tenant_A", "mat_101", "Party_A", "OWNS", "Prop_A", "doc_A", 1);
    provenance_graph.add_relationship_edge("org_tenant_B", "mat_201", "Party_A", "OWNS", "Prop_B", "doc_B", 2);

    const tenantA_results = provenance_graph.query_entity_graph("org_tenant_A", "Party_A");
    expect(tenantA_results.length).toBe(1);
    expect(tenantA_results[0].org_id).toBe("org_tenant_A");
  });
});
