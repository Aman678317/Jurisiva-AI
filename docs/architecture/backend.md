# Backend Architecture & Request Lifecycle Specification

## Framework & Request Pipeline
- **Framework**: FastAPI (Python 3.11+ async).
- **ORM / Persistence**: SQLAlchemy 2.0 async / Alembic migrations.
- **Task Queue**: Celery / ARQ backed by Redis.

## Request Lifecycle Pattern

```
HTTP Request
  ↓
Request ID & Trace ID Middleware (Generates `request_id`)
  ↓
Authentication Middleware (Validates JWT -> attaches `user`)
  ↓
Tenant & Matter Isolation Guard (Validates `organization_id` & `matter_id` membership)
  ↓
Pydantic Request Schema Validation (Rejects invalid body/params with HTTP 422)
  ↓
Application Service Handler (Coordinates domain repositories)
  ↓
Domain Rules Execution (Enforces business logic & unit conversions)
  ↓
Repository / DB Transaction (Executes scoped SQL queries)
  ↓
Audit Event Logger (Appends immutable audit record)
  ↓
Pydantic Response Schema Serialization (Strips internal fields)
  ↓
Structured Log Output (Logs status, latency, request_id)
```

## Service Module Boundaries

```
services/api/
 ├── app/
 │    ├── api/v1/ (Route Controllers)
 │    ├── core/ (Config, Security, DB session, Middleware)
 │    ├── modules/
 │    │    ├── identity/
 │    │    ├── matters/
 │    │    ├── documents/
 │    │    ├── search/
 │    │    ├── ai_gateway/
 │    │    ├── property/
 │    │    └── reports/
 │    ├── repositories/ (Database access layer)
 │    └── schemas/ (Pydantic DTOs)
```
