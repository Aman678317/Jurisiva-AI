# Enterprise Trust Center & Security Compliance Test Suite

from app.trust.trust_center import trust_center

describe("Chapter 22 Enterprise Security, Privacy & Trust Center", () => {
  test("TRST-001: Expose evidence-backed public trust summary", () => {
    const summary = trust_center.get_public_trust_summary();
    expect(summary.platform_name).toContain("Jurisiva AI");
    expect(summary.security_readiness_status).toBe("SECURITY_READY");
    expect(summary.security_controls.tenant_isolation).toContain("SEC-002");
  });

  test("TRST-002: Verify zero raw secret exposure in public trust summary", () => {
    const summaryJSON = JSON.stringify(trust_center.get_public_trust_summary());
    expect(summaryJSON).not.toContain("SECRET");
    expect(summaryJSON).not.toContain("PRIVATE_KEY");
    expect(summaryJSON).not.toContain("PASSWORD");
  });

  test("TRST-003: Subprocessor registry contains approved cloud & AI providers", () => {
    const summary = trust_center.get_public_trust_summary();
    expect(summary.subprocessors.length).toBeGreaterThanOrEqual(2);
    expect(summary.subprocessors[0].region).toBe("ap-south-1 (Mumbai)");
  });
});
