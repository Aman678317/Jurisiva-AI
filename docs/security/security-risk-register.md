# Security Risk Register & Remediation SLAs

## Active Risk Register

| Risk ID | Risk Description | Severity | Remediation SLA | Current Status |
| :--- | :--- | :---: | :---: | :---: |
| **SEC-RISK-01**| Malicious PDF upload vector (Polyglot / Script PDF) | HIGH | < 7 days | **MITIGATED** (PDF MIME & magic-bytes sandboxed) |
| **SEC-RISK-02**| Prompt injection via unverified document text | HIGH | < 7 days | **MITIGATED** (GovernedToolRegistry input filter) |
| **SEC-RISK-03**| Public government portal downtime during peak hours | MEDIUM | Accepted Risk | **MITIGATED** (Transparent circuit breaker fallback) |
