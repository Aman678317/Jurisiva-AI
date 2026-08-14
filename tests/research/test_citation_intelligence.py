# Precedent Citation & Evidence Intelligence Test Suite

from app.research.citation_graph import citation_graph_engine
from app.research.evidence_intelligence import evidence_intelligence_engine

describe("Chapter 21 Advanced Legal Research & Citation Graph", () => {
  test("RSC-001: Add precedent relationship edge with complete provenance", () => {
    const prov = { document_id: "sc_order_2024", page: 4, paragraph: 12 };
    const edge = citation_graph_engine.add_precedent_edge("org_001", "Case_A_v_State", "OVERRULES", "Case_B_v_State", prov);
    expect(edge.edge_id).toBeDefined();
    expect(edge.relationship).toBe("OVERRULES");
    expect(edge.provenance.page).toBe(4);
  });

  test("RSC-002: Zero cross-tenant citation graph traversal", () => {
    citation_graph_engine.add_precedent_edge("org_002", "Case_Unauth", "CITES", "Case_Ref", { page: 1 });

    const tenantA = citation_graph_engine.get_precedent_chain("org_001", "Case_Unauth");
    expect(tenantA.length).toBe(0);

    const tenantB = citation_graph_engine.get_precedent_chain("org_002", "Case_Unauth");
    expect(tenantB.length).toBe(1);
  });

  test("RSC-003: Citation locator precision validation requiring exact page number", () => {
    const invalidLoc = evidence_intelligence_engine.evaluate_citation_precision("Adverse possession claim", { page: 0 }, "Text snippet");
    expect(invalidLoc.status).toBe("UNVERIFIED");

    const validLoc = evidence_intelligence_engine.evaluate_citation_precision("Adverse possession claim", { page: 3 }, "12 years continuous possession proven.");
    expect(validLoc.status).toBe("SUPPORTED");
  });
});
