# Security, Privacy & AI Governance Test Suite

from app.security.model_registry import model_registry
from app.security.disaster_recovery import dr_simulator
from app.security.red_team import red_team_verifier
from app.integrations.orchestrator import SSRFSecurityGuard

describe("Chapter 12 Security, Privacy & AI Governance Assurance", () => {
  test("SEC-001: Model Registry enforces explicit approval & workflow policy", () => {
    expect(model_registry.is_model_approved("gpt-4o-mini", "PROPERTY_DUE_DILIGENCE")).toBe(true);
    expect(model_registry.is_model_approved("unapproved-model-v99")).toBe(false);
    expect(model_registry.is_model_approved("gpt-4o-mini", "UNAPPROVED_WORKFLOW")).toBe(false);
  });

  test("SEC-002: Red-Team Tenant Isolation & Zero Leakage", () => {
    const auditRes = red_team_verifier.verify_tenant_isolation("org_001", "org_002");
    expect(auditRes.status).toBe("PASS");
    expect(auditRes.auth_guard_blocked).toBe(true);
    expect(auditRes.search_engine_blocked).toBe(true);
    expect(auditRes.unauthorized_records_leaked).toBe(0);
  });

  test("SEC-003: SSRF Security Guard blocks private IP ranges", () => {
    expect(SSRFSecurityGuard.validate_external_url("http://127.0.0.1:5432")).toBe(false);
    expect(SSRFSecurityGuard.validate_external_url("http://localhost:9000")).toBe(false);
    expect(SSRFSecurityGuard.validate_external_url("http://169.254.169.254/latest/meta-data")).toBe(false);
    expect(SSRFSecurityGuard.validate_external_url("https://ecourts.gov.in/services")).toBe(true);
  });

  test("SEC-004: Disaster Recovery & Backup Restore Drill Simulation", () => {
    const drRes = dr_simulator.run_restore_test("snap_2026_08_14");
    expect(drRes.status).toBe("PASS");
    expect(drRes.database_restored).toBe(true);
    expect(drRes.storage_restored).toBe(true);
    expect(drRes.tenant_integrity_passed).toBe(true);
    expect(drRes.measured_rto_seconds).toBeLessThan(10.0);
  });
});
