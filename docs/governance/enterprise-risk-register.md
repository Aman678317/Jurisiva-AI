# Enterprise Risk Register & Severity SLAs

## Active Risk Register

| Risk ID | Risk Category | Risk Description | Severity | Owner | Mitigation Controls | Residual Risk |
| :--- | :--- | :--- | :---: | :--- | :--- | :---: |
| **RISK-AI-01** | AI Governance | Hallucinated encumbrance statement in title deed | HIGH | AI Lead | Page-grounded verification (`EVL-001`) | LOW |
| **RISK-SEC-02** | Security | Cross-tenant data leak via vector search | HIGH | CTO | Strict `org_id` filter in Qdrant queries | LOW |
| **RISK-LEG-03** | Legal / Reg | DPDP Act non-compliance on personal data export | HIGH | Counsel | 30-day automated data export pipeline | LOW |

Every risk has a designated owner and quarterly review SLA.
