# System Architectural Boundaries

## Overview
Explicit boundary definitions prevent security leaks, unintended coupling, and unhandled errors across system layers.

---

## Boundary Specifications

### 1. Frontend Boundary
- **INPUT**: User mouse/keyboard actions, form submissions, document file selection.
- **OUTPUT**: Rendered React UI components, PDF canvas rendering, API HTTP requests.
- **AUTHORIZATION**: Client-side route guards (UX level only; non-authoritative).
- **VALIDATION**: Form input schema validation (Zod / TypeScript).
- **ERROR HANDLING**: React Error Boundaries + Toast notifications.
- **OBSERVABILITY**: Anonymous user event telemetry (`product-analytics-events`).

### 2. API Boundary (HTTP / REST Gateway)
- **INPUT**: HTTP Requests (JSON payloads, multipart file uploads, Bearer JWTs).
- **OUTPUT**: JSON API responses, HTTP status codes, safe error contracts.
- **AUTHORIZATION**: Server-side JWT authentication & RBAC middleware checks.
- **VALIDATION**: Pydantic schema validation; multipart file type & size checks.
- **ERROR HANDLING**: Centralized HTTP exception handlers returning standard error contracts.
- **OBSERVABILITY**: Middleware logging `request_id`, endpoint, status, duration.

### 3. Domain Boundary (Application Logic)
- **INPUT**: Validated DTOs from API controllers.
- **OUTPUT**: Domain entity models, business calculation results.
- **AUTHORIZATION**: Scope verification (`organization_id` & `matter_id` matching).
- **VALIDATION**: Domain invariant enforcement (e.g. extent normalization check).
- **ERROR HANDLING**: Custom domain exceptions (`MatterNotFoundError`, `ExtentMismatchError`).
- **OBSERVABILITY**: Structured logs with trace IDs.

### 4. AI & Prompt Injection Boundary
- **INPUT**: Retrived context chunks + user query + strict system prompt.
- **OUTPUT**: Generated Markdown text + inline citation badges `[Doc, Page]`.
- **AUTHORIZATION**: System prompts forbid external tool access unless authorized by backend server.
- **VALIDATION**: Untrusted document text wrapped in XML tags (`<source_content>`); citation validator checks page bounds.
- **ERROR HANDLING**: Fallback to "Insufficient evidence in uploaded documents" if retrieval fails.
- **OBSERVABILITY**: Log token count, latency, model ID, and `ai_run_id`.

### 5. Data & Storage Boundary
- **INPUT**: SQL queries with explicit parameter bindings; Object storage stream.
- **OUTPUT**: Database record tuples; Binary file byte streams.
- **AUTHORIZATION**: SQL query WHERE clauses scoped by `organization_id` & `matter_id`.
- **VALIDATION**: DB column constraints, foreign key checks, unique indexes.
- **ERROR HANDLING**: Database transaction rollback on error.
- **OBSERVABILITY**: DB connection pool metrics, query execution timing.

### 6. Worker & Background Job Boundary
- **INPUT**: Enqueued job payloads (`job_id`, `matter_id`, `doc_id`).
- **OUTPUT**: Processed OCR text, vector chunks, job status updates.
- **AUTHORIZATION**: Worker validates job token against database before execution.
- **VALIDATION**: Idempotency key verification to prevent duplicate task runs.
- **ERROR HANDLING**: Exponential backoff retries (max 3 attempts); Dead-Letter Queue (DLQ).
- **OBSERVABILITY**: Task queue depth, job duration, failure rate metrics.
