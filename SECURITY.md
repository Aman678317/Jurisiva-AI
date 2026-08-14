# Security Architecture & Data Protection

## Security Guarantees
- **Data Isolation**: Strict matter-level logical tenant separation in database queries.
- **Encryption**: AES-256 for files at rest; TLS 1.3 in transit.
- **Access Control**: Role-Based Access Control (Admin, Lead Advocate, Associate, Read-Only Auditor).
- **Audit Logging**: Immutable event log tracking every file access, query, prompt, and export.
- **Data Retention & Scrubbing**: Workspace deletion purges vector index chunks and raw files completely.
