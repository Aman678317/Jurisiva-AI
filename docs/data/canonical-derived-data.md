# Canonical vs Derived vs Inferred Data Classification

## Data Provenance Classification Rules

| Data Classification | Description | Promotion Rule | Example |
| :--- | :--- | :--- | :--- |
| **CANONICAL** | Ground-truth facts directly from verified official sources or advocate inputs | Cannot be overwritten by AI inference | Verified Kaveri 2.0 RTC Survey No. 42/1 |
| **DERIVED** | Facts extracted mechanically from original documents (OCR, chunking) | Traceable 1:1 to original document & page | Text extracted from Page 2 of Sale Deed |
| **INFERRED** | AI-generated hypotheses, predicted entity matches, or chain of title timeline suggestions | Always marked `UNVERIFIED` until human advocate review | Copilot suggested ownership transition date |
| **TEMPORARY** | Short-lived context windows or vector search cache candidates | Purged after query execution | RAG prompt context string |

No AI prediction can be automatically promoted from `INFERRED` to `CANONICAL` without explicit advocate review.
