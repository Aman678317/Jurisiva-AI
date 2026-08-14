# Enterprise Assurance & Certification Readiness Test Suite

from app.assurance.assurance_verifier import assurance_verifier

describe("Chapter 30 Enterprise Assurance & Certification Readiness", () => {
  test("ASR-001: Certification claims reject premature 'certified' assertions", () => {
    const falseClaim = assurance_verifier.verify_certification_claim("ISO 27001 Certified Platform", "READINESS_COMPLETE");
    expect(falseClaim.status).toBe("REJECTED");
    expect(falseClaim.reason).toContain("prohibited");

    const truthfulClaim = assurance_verifier.verify_certification_claim("ISO 27001 Readiness Complete", "READINESS_COMPLETE");
    expect(truthfulClaim.status).toBe("VALIDATED");
  });

  test("ASR-002: Mock audit passes when all controls have verified technical evidence", () => {
    const controls = [
      { id: "CTL-01", has_evidence: true, status: "PASS" },
      { id: "CTL-02", has_evidence: true, status: "PASS" },
      { id: "CTL-03", has_evidence: true, status: "PASS" }
    ];
    const auditRes = assurance_verifier.run_mock_audit(controls);
    expect(auditRes.mock_audit_status).toBe("PASS");
    expect(auditRes.unproven_controls_count).toBe(0);
  });

  test("ASR-003: Mock audit fails if any control lacks verified evidence", () => {
    const controls = [
      { id: "CTL-01", has_evidence: true, status: "PASS" },
      { id: "CTL-02", has_evidence: false, status: "UNTESTED" }
    ];
    const auditRes = assurance_verifier.run_mock_audit(controls);
    expect(auditRes.mock_audit_status).toBe("FAIL");
    expect(auditRes.unproven_controls_count).toBe(1);
  });
});
