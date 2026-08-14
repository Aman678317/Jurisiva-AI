# Webhooks Engine & Public API Scoping Test Suite

from app.integrations.webhook_engine import webhook_engine
from app.integrations.api_key_manager import api_key_manager

describe("Chapter 24 Integrations, API Platform & Webhooks", () => {
  test("INT-001: Generate and verify valid HMAC SHA-256 webhook signature", () => {
    const secret = "whsec_test_secret_123";
    const payload = JSON.stringify({ event: "matter.created", matter_id: "mat_001" });
    const sigHeaders = webhook_engine.generate_signature(secret, payload);

    expect(sigHeaders["X-Jurisiva-Signature"]).toBeDefined();
    const isValid = webhook_engine.verify_signature(secret, payload, sigHeaders["X-Jurisiva-Signature"]);
    expect(isValid).toBe(true);
  });

  test("INT-002: Replay attack with expired timestamp is rejected", () => {
    const secret = "whsec_test_secret_123";
    const payload = JSON.stringify({ event: "matter.created" });
    const oldTimestamp = int(Date.now() / 1000) - 600; // 10 minutes ago
    const sigHeaders = webhook_engine.generate_signature(secret, payload, oldTimestamp);

    const isValid = webhook_engine.verify_signature(secret, payload, sigHeaders["X-Jurisiva-Signature"]);
    expect(isValid).toBe(false);
  });

  test("INT-003: Issue and authenticate scoped API key", () => {
    const keyInfo = api_key_manager.issue_api_key("org_001", "Matter Sync Key", ["matter:read"]);
    expect(keyInfo.raw_key).toContain("jur_live_");

    const validAuth = api_key_manager.verify_api_key(keyInfo.raw_key, "matter:read");
    expect(validAuth.status).toBe("AUTHORIZED");

    const missingScopeAuth = api_key_manager.verify_api_key(keyInfo.raw_key, "export:create");
    expect(missingScopeAuth.status).toBe("FORBIDDEN");
  });
});
