# Platform Scale & Performance Engineering Test Suite

from app.scale.tenant_governor import TenantResourceGovernor, tenant_governor

describe("Chapter 28 Platform Scale, Performance Engineering & Global Readiness", () => {
  test("SCL-001: Tenant concurrency throttling prevents noisy neighbor resource exhaustion", () => {
    const governor = new TenantResourceGovernor(2, 600);
    expect(governor.acquire_job_slot("org_heavy").status).toBe("ALLOWED");
    expect(governor.acquire_job_slot("org_heavy").status).toBe("ALLOWED");

    // 3rd concurrent request from org_heavy is throttled
    const throttled = governor.acquire_job_slot("org_heavy");
    expect(throttled.status).toBe("THROTTLED");
    expect(throttled.reason).toContain("exceeded max concurrent job capacity");

    // Separate tenant org_light is unimpeded
    expect(governor.acquire_job_slot("org_light").status).toBe("ALLOWED");
  });

  test("SCL-002: Tenant-safe cache key includes org_id prefix", () => {
    const key = TenantResourceGovernor.generate_tenant_cache_key("org_001", "matter", "mat_99");
    expect(key).toBe("cache:v1:org_org_001:matter_mat_99");
    expect(key).toContain("org_org_001");
  });
});
