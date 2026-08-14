# Institutional Governance & Risk Compliance Test Suite

from app.governance.compliance_verifier import compliance_verifier

describe("Chapter 29 Governance, Risk Management & Legal Operations", () => {
  test("GOV-001: Open-source license verification passes for approved licenses", () => {
    const pkgs = [
      { name: "fastapi", license: "MIT" },
      { name: "pydantic", license: "MIT" },
      { name: "sqlalchemy", license: "MIT" }
    ];
    const res = compliance_verifier.verify_license_compliance(pkgs);
    expect(res.status).toBe("PASS");
    expect(res.violations_count).toBe(0);
  });

  test("GOV-002: Prohibited copyleft license is flagged as violation", () => {
    const pkgs = [
      { name: "gpl_tool", license: "GPL-3.0" }
    ];
    const res = compliance_verifier.verify_license_compliance(pkgs);
    expect(res.status).toBe("FAIL");
    expect(res.violations_count).toBe(1);
  });

  test("GOV-003: High-risk AI actions require human approval and CRITICAL actions are rejected", () => {
    const highNoApproval = compliance_verifier.verify_ai_action_approval("HIGH", false);
    expect(highNoApproval.status).toBe("BLOCKED");

    const highApproved = compliance_verifier.verify_ai_action_approval("HIGH", true);
    expect(highApproved.status).toBe("APPROVED");

    const criticalAction = compliance_verifier.verify_ai_action_approval("CRITICAL", true);
    expect(criticalAction.status).toBe("REJECTED");
  });
});
