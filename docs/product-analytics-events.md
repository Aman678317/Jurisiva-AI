# Chapter 3 — Product Analytics Event Specifications

## Event Tracking Taxonomy

| Event Name | Trigger Condition | User Role | Properties Tracked | Purpose | Privacy / Security Guardrail |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `matter_created` | User submits new matter form. | Advocate / Associate | `matter_id`, `jurisdiction`, `doc_category` | Measure matter volume. | NO client names or personal data. |
| `document_uploaded` | File upload completes. | Advocate / Associate | `matter_id`, `file_format`, `file_size_mb`, `page_count` | Measure storage & bundle sizes. | NO document content or filename text. |
| `document_processed` | OCR & Indexing completes. | System / Worker | `matter_id`, `processing_duration_s`, `ocr_confidence` | Monitor system performance. | Technical metrics only. |
| `evidence_opened` | User clicks search snippet. | All members | `matter_id`, `doc_id`, `page_num` | Track evidence discovery. | NO snippet text logged. |
| `citation_opened` | User clicks `[Doc X, Page Y]`. | All members | `matter_id`, `citation_id`, `source_type` | Measure citation interaction. | Anonymous ID tracking only. |
| `copilot_run` | User submits Q&A prompt. | All members | `matter_id`, `prompt_length`, `preset_used` | Monitor Copilot usage. | NO prompt text sent to analytics. |
| `finding_verified` | Advocate clicks Verify on entity. | Advocate | `matter_id`, `entity_type`, `action` (`VERIFY`/`EDIT`) | Track HITL verification rate. | Action category only. |
| `conflict_inspected` | User opens red-flag alert. | Advocate | `matter_id`, `conflict_type` | Measure risk feature value. | High-level category only. |
| `report_generated` | User previews TSR report. | Advocate | `matter_id`, `template_id` | Track report workflow. | Category only. |
| `export_created` | User downloads DOCX/PDF TSR. | Advocate | `matter_id`, `format`, `unverified_count` | Measure primary output success. | Document format and metrics only. |
