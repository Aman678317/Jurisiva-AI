# Canonical Repository Folder Structure

```
legal/
 ├── apps/
 │    └── web/ (React Frontend Workspace)
 │         ├── src/
 │         ├── public/
 │         └── package.json
 │
 ├── services/
 │    └── api/ (FastAPI Core Backend)
 │         ├── app/
 │         ├── alembic/ (DB Migrations)
 │         └── requirements.txt
 │
 ├── workers/
 │    ├── ingestion_worker/
 │    └── ocr_worker/
 │
 ├── packages/
 │    ├── ui/ (Shared Design System Components)
 │    └── types/ (Shared TypeScript & Schema Definitions)
 │
 ├── infra/
 │    ├── docker-compose.yml
 │    └── Caddyfile
 │
 ├── docs/ (Complete 32-Chapter Documentation)
 │    ├── architecture/
 │    ├── database/
 │    ├── api/
 │    ├── development/
 │    └── prompts/
 │
 └── tests/
      ├── e2e/
      ├── integration/
      └── unit/
```
