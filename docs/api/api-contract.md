# API Contract Specifications (REST v1)

## Base URL Path: `/api/v1`

---

## 1. Authentication Endpoints
- `POST /auth/login`: Authenticates user credentials, returns HttpOnly JWT cookie & User DTO.
- `POST /auth/logout`: Clears session cookie.
- `GET /me`: Returns current user profile & organization memberships.

---

## 2. Matter Endpoints
- `GET /matters`: List all matters accessible to authenticated user.
  - *Query Params*: `status`, `page`, `limit`.
  - *Response*: `200 OK` `{ items: [MatterDTO], total: int }`.
- `POST /matters`: Create a new matter workspace.
  - *Request Body*: `{ title: str, client_name: str, survey_number: str, district: str, state: str }`.
  - *Response*: `201 Created` `MatterDTO`.
- `GET /matters/{matter_id}`: Fetch matter workspace details.

---

## 3. Document Endpoints
- `POST /matters/{matter_id}/documents`: Upload document bundle.
  - *Content-Type*: `multipart/form-data`.
  - *Body*: `files: UploadFile[]`, `hashes: string[]`.
  - *Response*: `202 Accepted` `{ job_id: str, uploaded_files: [DocumentDTO] }`.
- `GET /documents/{doc_id}`: Fetch document metadata & processing status.
- `GET /documents/{doc_id}/pages/{page_num}`: Fetch page image, OCR text, and bounding-box JSON.

---

## 4. Search & Evidence Endpoints
- `POST /matters/{matter_id}/search`: Execute hybrid vector + keyword search.
  - *Request Body*: `{ query: str, category_filter?: str, limit?: int }`.
  - *Response*: `200 OK` `{ results: [SearchResultDTO] }`.

---

## 5. Property Intelligence Endpoints
- `GET /matters/{matter_id}/property`: Fetch property schedule, timeline, and contradiction list.
  - *Response*: `200 OK` `PropertyIntelligenceDTO`.
- `POST /entities/{entity_id}/verify`: Verify or edit extracted property entity.
  - *Request Body*: `{ action: "VERIFY" | "EDIT" | "REJECT", verified_value?: str }`.
  - *Response*: `200 OK` `ExtractedEntityDTO`.

---

## 6. Copilot & Research Endpoints
- `POST /matters/{matter_id}/chat`: Citation-grounded RAG query stream.
  - *Request Body*: `{ query: str, preset?: str, doc_ids?: string[] }`.
  - *Response*: `200 OK` `Server-Sent Events (SSE)` streaming markdown chunks with inline citations.

---

## 7. Report Endpoints
- `POST /matters/{matter_id}/reports/generate`: Generate Title Search Report preview.
- `GET /matters/{matter_id}/reports/export`: Download formatted Title Search Report (`.docx` / `.pdf`).

---

## 8. Audit Endpoints
- `GET /matters/{matter_id}/audit`: Fetch paginated matter audit log events.

---

## Standard Error Contract

```json
{
  "error": {
    "code": "TENANT_ACCESS_DENIED",
    "message": "You do not have permission to access documents in this matter.",
    "request_id": "req_8f9a2b1c",
    "retryable": false,
    "details": {}
  }
}
```
