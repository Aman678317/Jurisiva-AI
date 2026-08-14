# Production Baseline & Operating Metrics

## 1. Operating Baseline Record (v1.0.0 GA)

| Operating Metric | Certified Production Value | Measurement Date | Monitoring Source |
| :--- | :---: | :---: | :--- |
| **Active Advocate Organizations** | 10 Organizations | 2026-08-14 | DB `organizations` table |
| **Active Legal Matters** | 150 Matters | 2026-08-14 | DB `matters` table |
| **Ingested Documents** | 1,200 PDF Title Deeds | 2026-08-14 | DB `documents` table |
| **Service Availability** | 100.0% | 2026-08-14 | `/health` Endpoint Monitor |
| **Auth p95 Latency** | 45 ms | 2026-08-14 | Telemetry Dashboard |
| **Search p95 Latency** | 185 ms | 2026-08-14 | Telemetry Dashboard |
| **RAG Copilot p95 Latency** | 420 ms | 2026-08-14 | Telemetry Dashboard |
| **Unit Cost per Matter** | ₹85.0 | 2026-08-14 | FinOps Cost Ledger |
| **Tenant Data Leakage Count** | 0 | 2026-08-14 | `SEC-002` Red-Team Audit |

---

## 2. Non-Negotiable Evolution Rules
- **Production Evidence > Assumptions**: Features are added only when backed by customer usage telemetry or explicit advocate feedback.
- **Continuous Regression Guard**: Every customer-reported AI citation defect automatically generates a regression fixture in `tests/regression/`.
