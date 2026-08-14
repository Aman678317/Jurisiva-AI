# Analytics Event Taxonomy

## Versioned Analytics Event Catalog (v1.0.0)

| Event Name | Schema Version | Payload Schema | Privacy Scope |
| :--- | :---: | :--- | :---: |
| `matter_created.v1` | `v1.0` | `{ org_id, matter_id, timestamp }` | Anonymous ID |
| `document_uploaded.v1` | `v1.0` | `{ org_id, document_id, file_type, page_count }` | No File Content |
| `search_executed.v1` | `v1.0` | `{ org_id, query_type, latency_ms, result_count }` | Query Sanitized |
| `report_exported.v1` | `v1.0` | `{ org_id, matter_id, report_format, duration_sec }` | Anonymous ID |
