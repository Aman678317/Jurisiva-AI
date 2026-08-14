# Backend Core & Security Integration Test Suite

from app.auth import auth_engine
from app.authorization import auth_guard
from app.audit import audit_logger
from app.storage import storage_adapter
from app.jobs import job_engine
from app.main import backend_server

describe("Backend Security & Core Services", () => {
  test("BE-TEST-001: Password hashing and verification", () => {
    const hashed = auth_engine.hash_password("Password123!");
    expect(hashed).not.toBe("Password123!");
    expect(auth_engine.verify_password("Password123!", hashed)).toBe(true);
    expect(auth_engine.verify_password("WrongPass", hashed)).toBe(false);
  });

  test("BE-TEST-002: Token creation and verification", () => {
    const tokenData = auth_engine.create_token("usr_001", "org_001", "LEAD_ADVOCATE");
    const verified = auth_engine.verify_token(tokenData.access_token);
    expect(verified).toBeDefined();
    expect(verified?.user_id).toBe("usr_001");
    expect(verified?.org_id).toBe("org_001");
  });

  test("BE-TEST-003: Server-side RBAC permission matrix", () => {
    expect(auth_guard.check_permission("LEAD_ADVOCATE", "matter.create")).toBe(true);
    expect(auth_guard.check_permission("ASSOCIATE", "matter.create")).toBe(false);
    expect(auth_guard.check_permission("AUDITOR", "document.delete")).toBe(false);
  });

  test("BE-TEST-004: Multi-Tenant Isolation & Cross-Tenant Rejection", () => {
    const isAllowed = auth_guard.verify_tenant_access("org_001", "org_002");
    expect(isAllowed).toBe(false); // Tenant A CANNOT access Tenant B data
    expect(auth_guard.verify_tenant_access("org_001", "org_001")).toBe(true);
  });

  test("BE-TEST-005: IDOR & Cross-Tenant Request Block in API", () => {
    const tokenData = auth_engine.create_token("usr_001", "org_001", "LEAD_ADVOCATE");
    const res = backend_server.handle_request(
      "/api/v1/matters/mat_001/documents",
      "POST",
      { Authorization: tokenData.access_token },
      { filename: "deed.pdf", byte_size: 1024, mime_type: "application/pdf" },
      { matter_org_id: "org_002" } // Attempting cross-tenant access to Org 002
    );
    expect(res.status).toBe("403 Forbidden");
    expect(res.error?.code).toBe("TENANT_ACCESS_DENIED");
  });

  test("BE-TEST-006: File Validation (MIME & Size Limits)", () => {
    const [validSize, sizeMsg] = storage_adapter.validate_file_metadata("large.pdf", 150 * 1024 * 1024, "application/pdf");
    expect(validSize).toBe(false);
    expect(sizeMsg).toContain("FILE_TOO_LARGE");

    const [validMime, mimeMsg] = storage_adapter.validate_file_metadata("script.exe", 1024, "application/x-msdownload");
    expect(validMime).toBe(false);
    expect(mimeMsg).toContain("UNSUPPORTED_FORMAT");
  });

  test("BE-TEST-007: Job State Machine Valid & Invalid Transitions", () => {
    const job = job_engine.create_job("org_001", "mat_001", "doc_001");
    expect(job.status).toBe("QUEUED");

    const [validTrans, _] = job_engine.transition_state(job.job_id, "VALIDATING");
    expect(validTrans).toBe(true);

    const [invalidTrans, err] = job_engine.transition_state(job.job_id, "READY"); // Cannot jump to READY directly from VALIDATING
    expect(invalidTrans).toBe(false);
    expect(err).toContain("INVALID_TRANSITION");
  });

  test("BE-TEST-008: Immutable Audit Logging", () => {
    const log = audit_logger.log_event("org_001", "usr_001", "Advocate Rajesh", "MATTER_CREATED", "Matter", "mat_999", "mat_999");
    expect(log.action).toBe("MATTER_CREATED");
    const orgLogs = audit_logger.get_matter_logs("org_001", "mat_999");
    expect(orgLogs.length).toBe(1);
  });
});
