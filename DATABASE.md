# Database Schema & Data Models

## Core Entities
- **Users**: `id`, `email`, `role`, `created_at`
- **Matters**: `id`, `title`, `client_name`, `state`, `created_by`, `created_at`
- **Documents**: `id`, `matter_id`, `filename`, `file_hash`, `mime_type`, `page_count`, `ocr_status`
- **DocumentPages**: `id`, `document_id`, `page_number`, `raw_text`, `ocr_confidence`, `image_url`
- **DocumentChunks**: `id`, `document_id`, `page_number`, `content`, `embedding` (vector), `bbox_json`
- **ExtractedEntities**: `id`, `matter_id`, `document_id`, `entity_type`, `entity_value`, `source_page`, `verification_status`
- **PropertyTimelines**: `id`, `matter_id`, `event_date`, `document_id`, `event_type`, `description`, `parties_involved`
- **AuditLogs**: `id`, `user_id`, `action`, `resource_type`, `resource_id`, `ip_address`, `timestamp`
