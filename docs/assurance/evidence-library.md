# Evidence Library Index & Retention Policy

## Evidence Item Catalog

| Evidence ID | Control Scope | Evidence Type | Timestamp / Source | Retention SLA |
| :--- | :--- | :--- | :--- | :--- |
| **`EVID-SEC-01`** | Access Control & Auth | Automated CI test report | Git SHA `chapter-29-institutional-governance` | 3 Years |
| **`EVID-DR-02`** | Disaster Recovery | DB restoration drill log | `services/api/app/security/disaster_recovery.py` | 3 Years |
| **`EVID-AI-03`** | AI Grounding & Citation | Golden dataset evaluation report | `tests/ai_quality/test_evaluation.py` | 3 Years |

All assurance evidence is store in immutable storage with cryptographic sha256 checksums.
