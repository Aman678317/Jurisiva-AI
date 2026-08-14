# Technical Debt Register & Scalability Prioritization

## Scalability Debt Matrix

| Debt Item | Impact | Priority | Remediation Plan |
| :--- | :--- | :---: | :--- |
| **Monolithic DB Connections** | High connection count at 1,000 RPM | P1 | Deploy PgBouncer pooler |
| **Synchronous OCR Thumbnailing**| Worker queue lag on 100+ page deeds | P2 | Move thumbnailing to async Celery task |
