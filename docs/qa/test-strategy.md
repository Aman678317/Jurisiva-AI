# QA Test Strategy & Quality Engineering Framework

## 1. Quality Engineering Pyramid

```text
               / \
              /   \   Layer 5: End-to-End User Journeys (E2E)
             / E2E \  [Critical Workflows: Upload -> OCR -> Copilot -> Export]
            /-------\
           /   API   \  Layer 4: API & Integration Contract Suite
          /-----------\ [FastAPI Routers, Auth Matrix, Tenant Scoping]
         /  PIPELINE   \  Layer 3: Ingestion, OCR & Hybrid RAG Benchmark
        /---------------\ [Indic OCR CER/WER, Citation Validation, RRF Search]
       /   UNIT & DATA   \  Layer 2: Core Unit & Database Integrity
      /-------------------\ [RBAC, Entity Resolution, State Machines]
     /  LINT & TYPECHECK   \  Layer 1: Static Analysis, Formatting & Types
    /-----------------------\ [TypeScript Strict, Python Mypy/Black]
```

---

## 2. Test Execution Schedule
- **Pre-Commit / Local**: Linting, Typecheck, Fast Unit Tests (< 10 seconds).
- **PR CI Gate**: Integration tests, API tests, Authorization Matrix, Security scans.
- **Pre-Release Stage**: Full E2E User Journeys, OCR/RAG Benchmark evaluation, Disaster Recovery drill.
