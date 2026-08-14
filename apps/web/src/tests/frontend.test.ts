// Frontend Component & E2E Test Suite Matrix

import { apiClient } from "../lib/api-client";
import { tokens } from "../tokens";

describe("Frontend Foundation & E2E Workflows", () => {
  test("FE-TEST-001: Design tokens color palette definition", () => {
    expect(tokens.colors.brand.primary).toBe("#0F172A");
    expect(tokens.colors.highlights.citationFill).toContain("rgba(254, 240, 138");
  });

  test("FE-TEST-002: API Client login contract test", async () => {
    const res = await apiClient.login("advocate@legal.in", "Password123!");
    expect(res.data).toBeDefined();
    expect(res.data?.user.role).toBe("LEAD_ADVOCATE");
  });

  test("FE-TEST-003: API Client matter retrieval test", async () => {
    const res = await apiClient.getMatters("org_001");
    expect(res.data?.length).toBeGreaterThan(0);
    expect(res.data?.[0].surveyNumber).toBe("42/1");
  });

  test("FE-TEST-004: Property Intelligence entity extraction and contradiction retrieval", async () => {
    const res = await apiClient.getPropertyIntelligence("mat_001");
    expect(res.data?.findings.length).toBeGreaterThan(0);
    expect(res.data?.contradictions.length).toBe(1);
    expect(res.data?.contradictions[0].severity).toBe("CRITICAL");
  });

  test("FE-TEST-005: Audit log event recording contract", async () => {
    const res = await apiClient.getAuditLogs("mat_001");
    expect(res.data?.length).toBe(2);
    expect(res.data?.[0].action).toBe("DOCUMENT_UPLOADED");
  });
});
