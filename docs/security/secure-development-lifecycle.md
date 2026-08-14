# Secure Development Lifecycle (SDLC) & Incident Response

## 1. Secure SDLC Gates
- **Design & Architecture**: Threat modeling mandatory for any new external integration or AI tool.
- **Code Review**: Every PR must verify tenant isolation, parameter sanitization, and SSRF allowlist protection.
- **Automated Security Gates**: Dependabot dependency scanning, secret scanning, and automated security test suite (`tests/security/test_security_compliance.py`).

## 2. Incident Response Plan (SEV-1 to SEV-4)
- **SEV-1 (Critical)**: Cross-tenant data leakage or unauthorized access to title deeds. *Action*: Immediate API suspension, token revocation, customer notification within 24 hrs.
- **SEV-2 (High)**: AI Gateway provider outage or SSRF attempt blocked. *Action*: Failover to secondary provider, SRE investigation.
- **SEV-3 (Medium)**: Transient OCR processing worker backlog.
- **SEV-4 (Low)**: Minor non-security logging anomaly.
