# Backend Application Server — FastAPI Gateway

import time
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Header, Query, Depends, Request
from fastapi.responses import JSONResponse

from app.auth import auth_engine
from app.authorization import auth_guard
from app.audit import audit_logger
from app.storage import storage_adapter
from app.jobs import job_engine

app = FastAPI(
    title="Jurisiva AI API",
    description="India-First Legal & Property Intelligence Platform API",
    version="1.0.0"
)

class FastAPIBackendServer:
    """Application Server handling backend API logic."""

    def handle_request(
        self,
        endpoint: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        body: Optional[Dict] = None,
        query_params: Optional[Dict] = None
    ) -> Dict:
        headers = headers or {}
        body = body or {}
        query_params = query_params or {}

        token = headers.get("Authorization", "").replace("Bearer ", "")
        session = auth_engine.verify_token(f"bearer_{token}") if token else None

        # 1. /api/v1/health
        if endpoint in ["/api/v1/health", "/health", "/"]:
            return {"status": "200 OK", "data": {"status": "HEALTHY", "db": "CONNECTED", "redis": "CONNECTED"}}

        # 2. /api/v1/auth/login
        if endpoint == "/api/v1/auth/login" and method == "POST":
            email = body.get("email", "")
            password = body.get("password", "")
            if email == "advocate@legal.in" and password == "Password123!":
                token_data = auth_engine.create_token("usr_001", "org_001", "LEAD_ADVOCATE")
                audit_logger.log_event("org_001", "usr_001", "Advocate Rajesh Sharma", "USER_LOGIN", "User", "usr_001")
                return {"status": "200 OK", "data": token_data}
            return {"status": "401 Unauthorized", "error": {"code": "INVALID_CREDENTIALS", "message": "Invalid credentials"}}

        # Protected Endpoint Check
        if not session:
            return {"status": "401 Unauthorized", "error": {"code": "UNAUTHENTICATED", "message": "Authentication required"}}

        user_id = session["user_id"]
        user_org_id = session["org_id"]
        role = session["role"]

        # 3. GET /api/v1/matters
        if endpoint == "/api/v1/matters" and method == "GET":
            if not auth_guard.check_permission(role, "matter.read"):
                return {"status": "403 Forbidden", "error": {"code": "PERMISSION_DENIED", "message": "Requires matter.read permission"}}
            return {
                "status": "200 OK",
                "data": [
                    {"id": "mat_001", "organization_id": user_org_id, "title": "Title Diligence — Sy No 42/1 Devanahalli", "client_name": "State Bank of India"}
                ]
            }

        # 4. POST /api/v1/matters (Create Matter)
        if endpoint == "/api/v1/matters" and method == "POST":
            if not auth_guard.check_permission(role, "matter.create"):
                return {"status": "403 Forbidden", "error": {"code": "PERMISSION_DENIED", "message": "Requires matter.create permission"}}
            title = body.get("title", "Untitled Matter")
            matter_id = f"mat_{int(time.time())}"
            audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "MATTER_CREATED", "Matter", matter_id)
            return {"status": "201 Created", "data": {"id": matter_id, "organization_id": user_org_id, "title": title}}

        # 5. POST /api/v1/matters/{matter_id}/documents (Upload Intent)
        if endpoint.startswith("/api/v1/matters/") and endpoint.endswith("/documents") and method == "POST":
            target_matter_org_id = query_params.get("matter_org_id", user_org_id)

            # Strict Tenant Isolation Check
            if not auth_guard.verify_tenant_access(user_org_id, target_matter_org_id):
                return {"status": "403 Forbidden", "error": {"code": "TENANT_ACCESS_DENIED", "message": "Cross-tenant access blocked."}}

            filename = body.get("filename", "deed.pdf")
            byte_size = body.get("byte_size", 1024)
            mime_type = body.get("mime_type", "application/pdf")

            valid, err_msg = storage_adapter.validate_file_metadata(filename, byte_size, mime_type)
            if not valid:
                return {"status": "400 Bad Request", "error": {"code": "INVALID_FILE", "message": err_msg}}

            storage_key = storage_adapter.generate_storage_key(user_org_id, "mat_001", "doc_001", "v1", filename)
            job = job_engine.create_job(user_org_id, "mat_001", "doc_001")
            audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "DOCUMENT_UPLOADED", "Document", "doc_001", "mat_001")

            return {"status": "202 Accepted", "data": {"job_id": job["job_id"], "storage_key": storage_key, "status": "QUEUED"}}

        return {"status": "404 Not Found", "error": {"code": "NOT_FOUND", "message": "Endpoint not found"}}

backend_server = FastAPIBackendServer()

# FastAPI HTTP Routes
@app.get("/")
@app.get("/health")
@app.get("/api/v1/health")
def health_check():
    res = backend_server.handle_request("/api/v1/health", "GET")
    return res["data"]

@app.post("/api/v1/auth/login")
async def login(request: Request):
    body = await request.json() if request.headers.get("content-type") == "application/json" else {}
    res = backend_server.handle_request("/api/v1/auth/login", "POST", body=body)
    if "error" in res:
        raise HTTPException(status_code=401, detail=res["error"])
    return res["data"]

@app.get("/api/v1/matters")
def get_matters(authorization: Optional[str] = Header(None)):
    headers = {"Authorization": authorization} if authorization else {}
    res = backend_server.handle_request("/api/v1/matters", "GET", headers=headers)
    if "error" in res:
        status_code = 403 if res["error"]["code"] == "PERMISSION_DENIED" else 401
        raise HTTPException(status_code=status_code, detail=res["error"])
    return res["data"]

@app.post("/api/v1/matters")
async def create_matter(request: Request, authorization: Optional[str] = Header(None)):
    body = await request.json()
    headers = {"Authorization": authorization} if authorization else {}
    res = backend_server.handle_request("/api/v1/matters", "POST", headers=headers, body=body)
    if "error" in res:
        status_code = 403 if res["error"]["code"] == "PERMISSION_DENIED" else 401
        raise HTTPException(status_code=status_code, detail=res["error"])
    return res["data"]

@app.post("/api/v1/matters/{matter_id}/documents")
async def upload_document(matter_id: str, request: Request, authorization: Optional[str] = Header(None), matter_org_id: Optional[str] = None):
    body = await request.json()
    headers = {"Authorization": authorization} if authorization else {}
    query_params = {"matter_org_id": matter_org_id} if matter_org_id else {}
    res = backend_server.handle_request(f"/api/v1/matters/{matter_id}/documents", "POST", headers=headers, body=body, query_params=query_params)
    if "error" in res:
        status_code = 403 if "DENIED" in res["error"]["code"] else 400
        raise HTTPException(status_code=status_code, detail=res["error"])
    return res["data"]
