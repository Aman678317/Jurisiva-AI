# Multi-Tenant Analytics Model & Metric Dictionary

## Metric Definitions

| Metric Name | Formula / Definition | Owner | Scope |
| :--- | :--- | :--- | :--- |
| **`title_search_completion_time`** | `time(report_generated) - time(deed_uploaded)` | Product Lead | Tenant Isolated |
| **`citation_grounding_rate`** | `count(valid_citations) / count(total_citations)` | AI Quality Lead | Platform Global |
| **`entity_resolution_accuracy`**| `count(verified_merges) / count(total_merges)` | Data Architect | Platform Global |
