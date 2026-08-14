# External Data Sources & India Integration Test Suite

from app.integrations.registry import source_registry
from app.integrations.mock_adapters import mock_court_adapter, mock_property_adapter
from app.integrations.orchestrator import research_orchestrator, SSRFSecurityGuard

describe("Chapter 11 External Research & India Integrations", () => {
  test("IND-001: Source Registry authority level lookup", () => {
    const ecourtsSrc = source_registry.get_source("src_ecourts");
    expect(ecourtsSrc).toBeDefined();
    expect(ecourtsSrc?.authority_level).toBe("LEVEL_1");
    expect(ecourtsSrc?.is_official).toBe(true);
  });

  test("IND-002: Mock Court Adapter search and normalization", () => {
    const results = mock_court_adapter.search("104/2019", {});
    expect(results.length).toBe(1);
    expect(results[0].case_number).toBe("O.S. No. 104/2019");

    const record = mock_court_adapter.fetch(results[0].case_id);
    const normalized = mock_court_adapter.normalize(record);
    expect(normalized.canonical_type).toBe("COURT_ORDER");
    expect(normalized.provenance.content_hash).toBeDefined();
  });

  test("IND-003: Mock Property Adapter land record lookup", () => {
    const parcels = mock_property_adapter.search("42/1", {});
    expect(parcels.length).toBe(1);
    expect(parcels[0].survey_number).toBe("42/1");
    expect(parcels[0].owner_name).toContain("Krishnappa");

    const health = mock_property_adapter.health_check();
    expect(health.status).toBe("HEALTHY");
  });

  test("IND-004: SSRF URL Security Guard blocks private IP subnets", () => {
    expect(SSRFSecurityGuard.validate_external_url("http://localhost:8000")).toBe(false);
    expect(SSRFSecurityGuard.validate_external_url("http://127.0.0.1/admin")).toBe(false);
    expect(SSRFSecurityGuard.validate_external_url("http://169.254.169.254/latest/meta-data")).toBe(false);
    expect(SSRFSecurityGuard.validate_external_url("https://ecourts.gov.in/services")).toBe(true);
  });

  test("IND-005: Research Orchestrator tenant security and provenance", () => {
    const courtRes = research_orchestrator.execute_court_research("org_001", "mat_001", "104/2019");
    expect(courtRes.status).toBe("SUCCESS");
    expect(courtRes.verification_status).toBe("SOURCE_RETRIEVED");
    expect(courtRes.authority_level).toBe("LEVEL_1");

    const unauthorizedRes = research_orchestrator.execute_court_research("", "mat_001", "104/2019");
    expect(unauthorizedRes.status).toBe("FORBIDDEN");
  });
});
