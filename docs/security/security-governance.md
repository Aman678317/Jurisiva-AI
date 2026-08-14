# Security Governance & Asset Inventory

## Security Governance Structure

| Governance Role | Designated Owner | Core Responsibilities |
| :--- | :--- | :--- |
| **Security Owner** | CTO / Head of Security | Overall security architecture, threat modeling, & incident escalation |
| **Engineering Owner** | Lead Backend Engineer | Secret management, patch SLAs, CI/CD security scanning, & key rotation |
| **Privacy Owner** | Compliance Lead / Counsel | DPDP Act alignment, data classification, & subprocessor governance |
| **Incident Owner** | SRE Lead | SEV-1 to SEV-4 security incident command & postmortem execution |

---

## Critical Asset Inventory

| Asset Name | Asset Type | Environment | Sensitivity Level | Encryption Status |
| :--- | :--- | :--- | :---: | :---: |
| **PostgreSQL 16 DB** | Relational Database | Production | `HIGHLY_SENSITIVE` | AES-256 (At-Rest) / TLS 1.3 (In-Transit) |
| **MinIO / S3 Store** | Object Storage | Production | `HIGHLY_SENSITIVE` | SSE-S3 AES-256 Encrypted |
| **Redis Broker** | Cache & Queue | Production | `CONFIDENTIAL` | TLS 1.3 & Password Auth |
| **API Secret Keys** | Credentials | Secret Manager | `HIGHLY_SENSITIVE` | Rotated & Environment Injected |
