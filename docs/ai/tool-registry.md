# Tool Registry & Permission Boundaries

## Governed Tool Catalog

| Tool Name | Purpose | Permission Level | Input Schema | Risk Level | Human Approval Required? |
| :--- | :--- | :---: | :--- | :---: | :---: |
| `search_matter_documents` | Hybrid BM25+vector search | READ | `{ query: str, limit: int }` | LOW | NO |
| `get_page_ocr_text` | Fetch OCR page text | READ | `{ document_id: str, page: int }` | LOW | NO |
| `propose_report_draft` | Propose title report section | PROPOSE | `{ section: str, draft: str }` | MEDIUM | YES |
| `export_data_zip` | Organization data export | EXPORT | `{ org_id: str }` | HIGH | MANDATORY |

Tools without registered input schemas are rejected at plan validation.
