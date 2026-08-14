# Data Intelligence Layer Architecture

## Data Tier Separation

```mermaid
graph TD
    Source[Raw Source PDFs / Public Records] --> Canonical[Canonical Database: PostgreSQL 16]
    Canonical --> Derived[Derived Intelligence Tier]
    Derived --> Vector[Vector Acceleration Store]
    Derived --> Graph[Temporal Knowledge Graph]
    Derived --> Analytics[Analytics Data Mart]
    Derived --> Decision[Explainable Decision Support Engine]
```

---

## Tier Principles
1. **Canonical Tier**: Authoritative ground-truth data (documents, matter metadata, RBAC memberships).
2. **Derived Tier**: AI-generated summaries, extracted entities, and vector embeddings. Derived objects MUST reference canonical source ID and page locator.
3. **Analytics Tier**: Aggregated product usage and matter progress metrics. Strictly tenant-isolated.
