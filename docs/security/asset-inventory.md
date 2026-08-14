# Asset Inventory & Classification

## Asset Classification Table

| Asset Name | Classification | Storage Location | Encryption | Retention Period | Deletion Method |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Original Title Deeds** | CONFIDENTIAL | Object Storage (`tenants/{org_id}/...`) | AES-256 at rest, TLS 1.3 in transit | Duration of active matter + 7 years | Cryptographic wipe |
| **Extracted OCR Pages** | CONFIDENTIAL | PostgreSQL `document_pages` | AES-256 at rest | Linked to Document lifecycle | Cascading DB delete |
| **Vector Embeddings** | CONFIDENTIAL | PostgreSQL `document_chunks` | AES-256 at rest | Derived artifact; rebuildable | SQL transaction delete |
| **AIRun Telemetry** | INTERNAL | PostgreSQL `ai_runs` | AES-256 at rest | 1 year | Automated cleanup |
| **User Credentials** | SENSITIVE | PostgreSQL `users` | PBKDF2 SHA-256 salted hash | Duration of account | Hard DB deletion |
| **Application Secrets** | HIGHLY SENSITIVE| Environment Variables / Vault | Encrypted in memory | Rotation every 90 days | Immediate key purge |
