# Operations & Incident Management Test Suite

from app.operations.ai_kill_switch import ai_kill_switch
from app.operations.incident_command import incident_command
from app.operations.telemetry_dashboard import telemetry_dashboard

describe("Chapter 15 Production Operations & Hypercare Suite", () => {
  test("OPS-101: AI Kill Switch disables feature cleanly", () => {
    expect(ai_kill_switch.is_feature_enabled("AI_COPILOT_ENABLED")).toBe(true);

    const disableRes = ai_kill_switch.disable_feature("AI_COPILOT_ENABLED", "Provider Outage", "usr_admin");
    expect(disableRes.status).toBe("DISABLED");
    expect(ai_kill_switch.is_feature_enabled("AI_COPILOT_ENABLED")).toBe(false);

    ai_kill_switch.enable_feature("AI_COPILOT_ENABLED", "usr_admin");
    expect(ai_kill_switch.is_feature_enabled("AI_COPILOT_ENABLED")).toBe(true);
  });

  test("OPS-102: Incident Command Engine lifecycle flow", () => {
    const inc = incident_command.declare_incident("SEV-1", "Mock Test Incident", "usr_admin");
    expect(inc.status).toBe("DECLARED");
    expect(inc.severity).toBe("SEV-1");

    const resolved = incident_command.resolve_incident(inc.incident_id, "Patch Deployed");
    expect(resolved.status).toBe("RESOLVED");
    expect(resolved.root_cause).toBe("Patch Deployed");
  });

  test("OPS-103: Live telemetry SLA metrics validation", () => {
    const metrics = telemetry_dashboard.get_live_metrics();
    expect(metrics.service_availability).toBe(1.00);
    expect(metrics.auth_p95_ms).toBeLessThan(150);
    expect(metrics.rag_p95_ms).toBeLessThan(1500);
    expect(metrics.unit_cost_inr).toBeLessThan(120.0);
  });
});
