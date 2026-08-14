# ADR-001: Application Architecture — Modular Monolith

## CONTEXT
We require an application architecture for an India-first legal/property AI platform that supports rapid iteration, strict security boundaries, low operational complexity for a solo founder, and high maintainability.

## OPTIONS
1. **Distributed Microservices**: Separate services for Auth, Matters, Documents, OCR, Search, RAG, and Reports.
2. **Modular Monolith**: Single codebase with strict internal module boundaries + separate background workers for async processing.
3. **Serverless Functions**: Pure lambda/serverless backend.

## DECISION
Option 2: **Modular Monolith**.

## RATIONALE
A modular monolith provides clean domain separation without the network latency, deployment overhead, distributed tracing complexity, and infrastructure cost of microservices. Domain modules (identity, matters, documents, search, AI gateway) communicate via explicit internal interfaces. High-load asynchronous tasks (OCR, chunking, vector indexing) run on dedicated background worker processes.

## TRADE-OFFS
- Monolith requires disciplined code organization to prevent module coupling.
- Addressed by enforcing repository interface contracts between modules.

## COST
₹0 additional infra cost (Runs on a single VPS node).

## SECURITY
Simplified security perimeter; central middleware enforces tenant isolation and RBAC.

## MIGRATION PATH
Individual domain modules (e.g. OCR pipeline or Search service) can be extracted into standalone microservices if traffic or resource demands require it.

## REVIEW TRIGGER
Monthly active matters > 10,000 or backend API p95 latency > 500ms.
