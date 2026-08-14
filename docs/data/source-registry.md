# Source Registry & Data Lineage Specifications

## 1. Source Registry Schema
```json
{
  "source_id": "src_ecourts_01",
  "name": "eCourts Services India",
  "authority_level": "LEVEL_1",
  "jurisdiction": "IN-NATIONAL",
  "access_method": "PUBLIC_WEB_PORTAL",
  "freshness_policy_hours": 24,
  "enabled": true
}
```

## 2. Data Lineage Traceability
Every external record normalized into canonical property models retains:
- `source_id`: Registry ID of external provider
- `retrieved_at`: UTC timestamp of retrieval
- `content_hash`: SHA-256 hash of raw response
- `raw_reference`: Original JSON/HTML payload preserved for audit
