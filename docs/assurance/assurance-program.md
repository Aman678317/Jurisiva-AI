# Enterprise Control Assurance Program & Scope

## Assurance Scope & Boundaries

```mermaid
graph TD
    Scope[Enterprise Assurance Scope] --> Infra[AWS ap-south-1 Cloud & IAM]
    Scope --> App[FastAPI Backend & Next.js Frontend]
    Scope --> Data[PostgreSQL 16 & MinIO S3 Storage]
    Scope --> AI[LiteLLM Gateway & Governed AI Agents]
    Scope --> Vendors[Subprocessor Vendors Catalog]
```

---

## Assurance Principles
1. **Evidence Over Claims**: Written policy is insufficient; every control requires dateable, reproducible technical evidence.
2. **Truthful Certification Status**: Explicitly distinguish `CERTIFICATION_READY` (Internal verification complete) from `CERTIFIED` (Independent third-party audit completed).
3. **Continuous Verification**: Controls tested automatically in CI/CD and security regression suites on every build.
