# Enterprise Scale & Governance Test Suite

from app.scale.capacity_planner import capacity_planner
from app.scale.enterprise_governance import enterprise_governance

describe("Chapter 16 Enterprise Hardening, Scale & Governance", () => {
  test("SCL-001: Capacity Planner calculates 10x and 100x scale thresholds", () => {
    const scale10x = capacity_planner.calculate_scale_capacity(10.0);
    expect(scale10x.target_api_rpm).toBe(15000);
    expect(scale10x.use_pgbouncer).toBe(true);

    const scale100x = capacity_planner.calculate_scale_capacity(100.0);
    expect(scale100x.target_api_rpm).toBe(150000);
    expect(scale100x.recommended_db_connections).toBe(200);
  });

  test("SCL-002: Enterprise Data Export requires ADMIN/OWNER role", () => {
    const validExport = enterprise_governance.generate_organization_export("org_001", "ADMIN");
    expect(validExport.status).toBe("SUCCESS");
    expect(validExport.export_format).toBe("JSON_ZIP");

    const invalidExport = enterprise_governance.generate_organization_export("org_001", "ASSOCIATE");
    expect(invalidExport.status).toBe("FORBIDDEN");
  });

  test("SCL-003: SCIM Deprovisioning blocks disabled accounts", () => {
    expect(enterprise_governance.verify_scim_deprovisioning("DISABLED")).toBe(true);
    expect(enterprise_governance.verify_scim_deprovisioning("SUSPENDED")).toBe(true);
    expect(enterprise_governance.verify_scim_deprovisioning("ACTIVE")).toBe(false);
  });
});
