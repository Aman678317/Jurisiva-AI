# HMAC Signed Webhooks Architecture & Replay Protection

## HMAC SHA-256 Signature Verification
Every outbound webhook delivery payload contains an `X-Jurisiva-Signature` header calculated as:

```text
X-Jurisiva-Signature: t=1786729200,v1=HMAC-SHA256(secret, "1786729200.payload_json")
```

---

## Replay Protection & Re-delivery
- **Timestamp Threshold**: Receivers must verify `t` is within 300 seconds of current system time.
- **Bounded Exponential Backoff**: Retries executed up to 5 times before moving to `DEAD_LETTER` state.
- **SSRF Prevention**: Webhook destination URLs checked via `SSRFSecurityGuard` to block internal IP ranges.
