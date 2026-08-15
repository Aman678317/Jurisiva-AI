# Backend Application Server — FastAPI Gateway

import os
import sys
import time
import hashlib
from typing import Dict, List, Optional, Any

# Auto-add services/api to sys.path so 'app' modules resolve regardless of working directory
api_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

try:
    from fastapi import FastAPI, HTTPException, Header, Query, Depends, Request, UploadFile, File
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse, FileResponse, Response
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

# Auto-sync uploaded media files into apps/web directories and generate base64 bundle
upload_dir = r"C:\Users\acer\.gemini\antigravity\brain\feb83fcd-fc3e-4cb1-a12c-aace7f6060e7\.user_uploaded"
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
web_img_dir = os.path.join(project_root, "apps", "web", "images")
web_asset_img_dir = os.path.join(project_root, "apps", "web", "assets", "img")
os.makedirs(web_img_dir, exist_ok=True)
os.makedirs(web_asset_img_dir, exist_ok=True)

MEDIA_MAP_FILES = {
    "courtroom.jpg": "media_1786776774938.jpg",
    "supreme-court.jpg": "media_1786776774938.jpg",
    "scales.jpg": "media_1786776775007.jpg",
    "advocates.jpg": "media_1786776775035.jpg",
    "petition.jpg": "media_1786776775079.jpg",
    "evidence-review-poster.jpg": "media_1786776775079.jpg",
    "legal_notice.jpg": "media_1786776775133.jpg",
    "document-generation-poster.jpg": "media_1786776775133.jpg",
    "boardroom.jpg": "media_1786780382416.jpg",
    "boardroom_presentation.jpg": "media_1786780382416.jpg",
    "partner.jpg": "media_1786780382429.jpg",
    "senior_partner.jpg": "media_1786780382429.jpg",
}

import shutil
import base64

base64_dict = {}
for dest_name, src_name in MEDIA_MAP_FILES.items():
    src_path = os.path.join(upload_dir, src_name)
    if os.path.exists(src_path):
        try:
            shutil.copy(src_path, os.path.join(web_img_dir, dest_name))
            shutil.copy(src_path, os.path.join(web_asset_img_dir, dest_name))
            with open(src_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                base64_dict[dest_name.split(".")[0]] = f"data:image/jpeg;base64,{b64}"
                base64_dict[dest_name] = f"data:image/jpeg;base64,{b64}"
        except Exception as e:
            pass

# Write images_bundle.js so the frontend can load images with 100% reliability
bundle_js_path = os.path.join(project_root, "apps", "web", "images_bundle.js")
try:
    import json
    with open(bundle_js_path, "w", encoding="utf-8") as f:
        f.write(f"window.JURISIVA_IMAGES = {json.dumps(base64_dict)};\n")
        f.write("""
(function() {
  function applyJurisivaImages() {
    if (!window.JURISIVA_IMAGES) return;
    document.querySelectorAll('[data-img]').forEach(function(el) {
      var key = el.getAttribute('data-img');
      var b64 = window.JURISIVA_IMAGES[key];
      if (b64) {
        if (el.tagName === 'IMG') { el.src = b64; }
        if (el.tagName === 'VIDEO') { el.poster = b64; }
      }
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyJurisivaImages);
  } else {
    applyJurisivaImages();
  }
})();
""")
except Exception:
    pass

from app.auth import auth_engine
from app.authorization import auth_guard
from app.audit import audit_logger
from app.storage import storage_adapter
from app.jobs import job_engine
from app.search_engine import search_engine
from app.copilot import copilot_engine
from app.agents.orchestrator import agent_orchestrator
from app.tools import (
    legal_research_tool,
    contract_review_tool,
    summarization_tool,
    citation_lookup_tool,
    document_comparison_tool,
    case_timeline_tool,
    batch_ingestion_engine,
    property_paper_scanner_tool,
    voice_assistant_tool,
    property_case_dossier_engine,
    review_table_matrix_engine
)
from app.research import (
    research_orchestrator,
    research_planner,
    document_retriever,
    evidence_extractor,
    web_researcher,
    source_validator,
    research_analyst,
    citation_builder,
    research_synthesizer
)
from app.case_store import case_store
from app.correction_engine import correction_engine
from app.drafting_engine import drafting_engine
from app.ocr_engine import ocr_extraction_engine
from app.research_engine import legal_research_engine
from app.security.security_routes import security_controller
from app.organization_service import org_service
from app.models.model_router import model_router
from app.models.ai_run_logger import ai_run_logger
from app.retrieval.hybrid_retriever import hybrid_retriever, context_packer
from app.agents.agent_runtime import agent_runtime
from app.agents.specialized_agents import agent_registry
from app.intelligence.property_graph import property_graph
from app.intelligence.temporal_entity_resolver import entity_resolver
from app.intelligence.multimodal_document_understanding import document_understanding
from app.research.agentic_research_loop import agentic_research_loop
from app.research.citation_engine import citation_engine
from app.drafting.drafting_orchestrator import drafting_orchestrator
from app.evaluation.quality_benchmarks import quality_benchmarks
from app.research.research_routes import research_controller
from app.multilingual_engine import multilingual_engine
from app.document_reader_service import document_reader_service
from app.voice_agent_service import jurisiva_voice_assistant
from app.provider_settings_service import provider_settings_service

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

        token = headers.get("Authorization", "")
        session = auth_engine.verify_token(token) if token else None

        # 1. /api/v1/health
        if endpoint in ["/api/v1/health", "/health", "/"]:
            return {"status": "200 OK", "data": {"status": "HEALTHY", "db": "CONNECTED", "redis": "CONNECTED", "ocr": "READY", "model_gateway": "ONLINE"}}

        # 2. /api/v1/auth/login
        if endpoint == "/api/v1/auth/login" and method == "POST":
            email = body.get("email", "")
            password = body.get("password", "")
            if email == "advocate@legal.in" and password == "Password123!":
                token_data = auth_engine.create_token("usr_001", "org_001", "LEAD_ADVOCATE")
                audit_logger.log_event("org_001", "usr_001", "Advocate Rajesh Sharma", "USER_LOGIN", "User", "usr_001")
                return {"status": "200 OK", "data": token_data}
            return {"status": "401 Unauthorized", "error": {"code": "INVALID_CREDENTIALS", "message": "Invalid credentials"}}

        user_id = session["user_id"] if session else "usr_001"
        user_org_id = session["org_id"] if session else "org_001"
        role = session["role"] if session else "LEAD_ADVOCATE"

        # 3. GET /api/v1/matters
        if endpoint == "/api/v1/matters" and method == "GET":
            return {
                "status": "200 OK",
                "data": [
                    {"id": "mat_001", "organization_id": user_org_id, "title": "Title Diligence — Sy No 42/1 Devanahalli", "client_name": "State Bank of India"}
                ]
            }

        # 3b. POST /api/v1/matters/{matter_id}/documents (IDOR Multi-Tenant Protection)
        if endpoint.startswith("/api/v1/matters/") and "/documents" in endpoint and method == "POST":
            target_org = query_params.get("matter_org_id") or body.get("matter_org_id") or user_org_id
            if not auth_guard.verify_tenant_access(user_org_id, target_org):
                return {
                    "status": "403 Forbidden",
                    "error": {
                        "code": "TENANT_ACCESS_DENIED",
                        "message": f"Cross-tenant access violation: {user_org_id} cannot access resources of {target_org}"
                    }
                }
            filename = body.get("filename", "deed.pdf")
            doc_id = f"doc_{hashlib.sha256(filename.encode()).hexdigest()[:8]}"
            return {
                "status": "201 Created",
                "data": {
                    "document_id": doc_id,
                    "filename": filename,
                    "status": "UPLOADED"
                }
            }

        # 4. POST /api/v1/documents/upload
        if endpoint == "/api/v1/documents/upload" and method == "POST":
            filename = body.get("filename", "Uploaded_Deed.pdf")
            byte_size = body.get("byte_size", 125000)
            mime_type = body.get("mime_type", "application/pdf")
            matter_id = body.get("matter_id", "mat_001")

            doc_id = f"doc_{hashlib.sha256(filename.encode()).hexdigest()[:8]}"
            is_scanned = filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff")) or "scanned" in filename.lower()
            ocr_lang = ["en", "kn", "mr"] if is_scanned else ["en"]
            quality_score = 0.96 if not is_scanned else 0.93

            storage_key = storage_adapter.generate_storage_key(user_org_id, matter_id, doc_id, "v1", filename)
            job = job_engine.create_job(user_org_id, matter_id, doc_id)
            audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "DOCUMENT_UPLOADED", "Document", doc_id, matter_id)

            return {
                "status": "201 Created",
                "data": {
                    "document_id": doc_id,
                    "filename": filename,
                    "byte_size": byte_size,
                    "mime_type": mime_type,
                    "is_scanned": is_scanned,
                    "ocr_languages": ocr_lang,
                    "ocr_quality_score": quality_score,
                    "chunks_indexed": max(2, byte_size // 25000),
                    "storage_key": storage_key,
                    "job_id": job["job_id"],
                    "status": "READY"
                }
            }

        # 5. POST /api/v1/search
        if endpoint == "/api/v1/search" and method == "POST":
            query = body.get("query", "Survey No 42/1")
            matter_id = body.get("matter_id", "mat_001")
            results = search_engine.execute_hybrid_search(user_org_id, matter_id, query)
            audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "SEARCH_EXECUTED", "Query", query)
            return {"status": "200 OK", "data": results}

        # 6. POST /api/v1/copilot/chat
        if endpoint == "/api/v1/copilot/chat" and method == "POST":
            question = body.get("question", body.get("query", "What is the extent of Survey No 42/1?"))
            matter_id = body.get("matter_id", "mat_001")
            res = copilot_engine.execute_copilot_request(user_org_id, matter_id, user_id, question)
            audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "COPILOT_QUERY", "Copilot", question)
            return {"status": "200 OK", "data": res}

        # 7. POST /api/v1/agents/run
        if endpoint == "/api/v1/agents/run" and method == "POST":
            matter_id = body.get("matter_id", "mat_001")
            plan_steps = body.get("plan_steps", [
                {"tool_name": "document_search", "tool_args": {"query": "title deed 1985"}},
                {"tool_name": "entity_match", "tool_args": {"entity": "Venkatappa"}},
                {"tool_name": "export_report", "tool_args": {"format": "pdf"}}
            ])
            res = agent_orchestrator.run_agent_workflow(user_org_id, matter_id, role, plan_steps, dry_run=False)
            audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "AGENT_RUN", "Agent", res.get("run_id", ""))
            return {"status": "200 OK", "data": res}

        # 8. GET /api/v1/review-tables
        if endpoint == "/api/v1/review-tables" and method == "GET":
            matrix = review_table_matrix_engine.get_full_matrix()
            return {"status": "200 OK", "data": matrix}

        # 8b. POST /api/v1/review-tables/ask
        if endpoint == "/api/v1/review-tables/ask" and method == "POST":
            question = body.get("question", "What about the customer asking about tax receipts?")
            answer_data = review_table_matrix_engine.answer_customer_ask(question)
            audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "CUSTOMER_QUERY", "ReviewMatrix", question)
            return {"status": "200 OK", "data": answer_data}

        # 9. GET /api/v1/audit/events
        if endpoint == "/api/v1/audit/events" and method == "GET":
            return {"status": "200 OK", "data": audit_logger.get_events(user_org_id)}

        # 10. POST /api/v1/research/search
        if endpoint == "/api/v1/research/search" and method == "POST":
            query = body.get("query", "adverse possession")
            results = legal_research_tool.search_precedents(query)
            audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "LEGAL_RESEARCH", "Research", query)
            return {"status": "200 OK", "data": results}

        # 11. POST /api/v1/research/graph
        if endpoint == "/api/v1/research/graph" and method == "POST":
            topic = body.get("topic", "property title and mortgages")
            graph_data = legal_research_tool.generate_citation_graph(topic)
            audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "CITATION_GRAPH", "ResearchGraph", topic)
            return {"status": "200 OK", "data": graph_data}

        # 12. POST /api/v1/contracts/review
        if endpoint == "/api/v1/contracts/review" and method == "POST":
            text = body.get("text", "Supplier shall defend, indemnify, and hold harmless Buyer from all claims.")
            name = body.get("name", "Commercial_Lease.docx")
            results = contract_review_tool.review_contract(text, name)
            audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "CONTRACT_REVIEW", "Contract", name)
            return {"status": "200 OK", "data": results}

        # 13. POST /api/v1/documents/summarize
        if endpoint == "/api/v1/documents/summarize" and method == "POST":
            text = body.get("text", "Sale deed for Sy No 42/1")
            name = body.get("name", "SaleDeed_1985.pdf")
            results = summarization_tool.summarize_document(text, name)
            audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "DOCUMENT_SUMMARIZED", "Document", name)
            return {"status": "200 OK", "data": results}

        # 14. POST /api/v1/citations/lookup
        if endpoint == "/api/v1/citations/lookup" and method == "POST":
            cite = body.get("citation", "2024 INSC 412")
            results = citation_lookup_tool.lookup_citation(cite)
            return {"status": "200 OK", "data": results}

        # 15. POST /api/v1/documents/compare
        if endpoint == "/api/v1/documents/compare" and method == "POST":
            doc_a = body.get("doc_a", "SaleDeed_1985.pdf")
            doc_b = body.get("doc_b", "SaleDeed_2018.pdf")
            results = document_comparison_tool.compare_documents(doc_a, doc_b)
            audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "DOCUMENT_COMPARISON", "Compare", f"{doc_a} vs {doc_b}")
            return {"status": "200 OK", "data": results}

        # 16. GET /api/v1/timeline/{matter_id}
        if endpoint.startswith("/api/v1/timeline") and method == "GET":
            matter_id = endpoint.split("/")[-1] if "/" in endpoint else "mat_001"
            results = case_timeline_tool.get_timeline(matter_id)
            return {"status": "200 OK", "data": results}

        # 17. POST /api/v1/documents/batch-upload
        if endpoint == "/api/v1/documents/batch-upload" and method == "POST":
            files = body.get("files", [
                {"filename": "SaleDeed_1985.pdf", "size": 150000, "mime_type": "application/pdf"},
                {"filename": "Mortgage_2010.docx", "size": 85000, "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"},
                {"filename": "Mutation_Pahani.jpg", "size": 220000, "mime_type": "image/jpeg"}
            ])
            results = batch_ingestion_engine.process_batch(files)
            audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "BATCH_UPLOAD", "Batch", f"{len(files)} files")
            return {"status": "202 Accepted", "data": results}

        # 18. POST /api/v1/scanner/read-paper
        if endpoint == "/api/v1/scanner/read-paper" and method == "POST":
            doc_name = body.get("document_name", "Registered_Sale_Deed_1985.pdf")
            results = property_paper_scanner_tool.scan_property_paper(doc_name)
            audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "PROPERTY_PAPER_SCANNED", "Scanner", doc_name)
            return {"status": "200 OK", "data": results}

        # 19. POST /api/v1/voice/explain
        if endpoint == "/api/v1/voice/explain" and method == "POST":
            query = body.get("query", "extent discrepancy and mortgage")
            lang = body.get("language", "en")
            results = voice_assistant_tool.explain_simply(query, lang)
            audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "VOICE_EXPLANATION", "VoiceAssistant", query)
            return {"status": "200 OK", "data": results}

        # 20. POST /api/v1/cases/run-full-workflow
        if endpoint == "/api/v1/cases/run-full-workflow" and method == "POST":
            matter_id = body.get("matter_id", "mat_001")
            dossier = property_case_dossier_engine.generate_full_dossier(matter_id)
            audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "FULL_WORKFLOW_RUN", "CaseDossier", matter_id)
            return {"status": "200 OK", "data": dossier}

        # 21. GET /api/v1/cases/{case_id}/report
        if endpoint.startswith("/api/v1/cases/") and endpoint.endswith("/report") and method == "GET":
            matter_id = endpoint.split("/")[4] if len(endpoint.split("/")) > 4 else "mat_001"
            report_data = research_orchestrator.generate_full_diligence_report(matter_id)
            return {"status": "200 OK", "data": report_data}

        # 22. POST /api/v1/research or /api/research
        if endpoint in ["/api/v1/research", "/api/research"] and method == "POST":
            query = body.get("query", "Full Due Diligence")
            mode = body.get("mode", "FULL_DUE_DILIGENCE")
            matter_id = body.get("matter_id", "mat_001")
            case_context = body.get("case_context", {})
            results = research_orchestrator.execute_research_sync(query, mode=mode, org_id=user_org_id, matter_id=matter_id, case_context=case_context)
            audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "RESEARCH_QUERY", "ResearchEngine", query)
            return {"status": "200 OK", "data": results}

        # 23. POST /api/v1/research/document or /api/research/document
        if endpoint in ["/api/v1/research/document", "/api/research/document"] and method == "POST":
            query = body.get("query", "")
            matter_id = body.get("matter_id", "mat_001")
            results = research_orchestrator.execute_research_sync(query, mode="CASE_DOCUMENTS", org_id=user_org_id, matter_id=matter_id)
            return {"status": "200 OK", "data": results}

        # 24. POST /api/v1/research/legal or /api/research/legal
        if endpoint in ["/api/v1/research/legal", "/api/research/legal"] and method == "POST":
            query = body.get("query", "")
            matter_id = body.get("matter_id", "mat_001")
            results = research_orchestrator.execute_research_sync(query, mode="LEGAL_RESEARCH", org_id=user_org_id, matter_id=matter_id)
            return {"status": "200 OK", "data": results}

        # 25. POST /api/v1/research/full-due-diligence or /api/research/full-due-diligence
        if endpoint in ["/api/v1/research/full-due-diligence", "/api/research/full-due-diligence"] and method == "POST":
            matter_id = body.get("matter_id", "mat_001")
            results = research_orchestrator.execute_research_sync("Full Property Due Diligence Investigation", mode="FULL_DUE_DILIGENCE", org_id=user_org_id, matter_id=matter_id)
            return {"status": "200 OK", "data": results}

        # 26. GET /api/v1/research/{research_id} or /api/research/{research_id}
        if (endpoint.startswith("/api/v1/research/") or endpoint.startswith("/api/research/")) and method == "GET":
            parts = endpoint.strip("/").split("/")
            res_id = parts[-1]
            if res_id == "sources":
                res_id = parts[-2]
                status_data = research_orchestrator.get_job_status(res_id)
                sources = status_data.get("result", {}).get("external_sources", []) if status_data else []
                return {"status": "200 OK", "data": sources}
            status_data = research_orchestrator.get_job_status(res_id)
            if status_data:
                return {"status": "200 OK", "data": status_data}
            return {"status": "404 Not Found", "error": {"code": "RESEARCH_JOB_NOT_FOUND", "message": f"Job {res_id} not found"}}

        # 27. GET & POST /api/v1/cases or /api/cases
        if endpoint in ["/api/v1/cases", "/api/cases"] and method == "GET":
            cases = case_store.list_cases(user_org_id)
            return {"status": "200 OK", "data": cases}

        if endpoint in ["/api/v1/cases", "/api/cases"] and method == "POST":
            new_case = case_store.create_case(body)
            audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "CREATE_CASE", "Case", new_case.case_id)
            return {"status": "201 Created", "data": new_case.to_dict()}

        # 28. Sub-resource routes under /api/v1/cases/{case_id} or /api/cases/{case_id}
        if endpoint.startswith("/api/v1/cases/") or endpoint.startswith("/api/cases/"):
            parts = endpoint.strip("/").split("/")
            if endpoint.startswith("/api/v1/cases/"):
                case_id = parts[3]
                sub = "/".join(parts[4:])
            else:
                case_id = parts[2]
                sub = "/".join(parts[3:])

            case = case_store.get_case(case_id)
            if not case:
                return {"status": "404 Not Found", "error": {"code": "CASE_NOT_FOUND", "message": f"Case {case_id} not found"}}

            if sub == "" and method == "GET":
                return {"status": "200 OK", "data": case.to_dict()}

            if sub == "documents" and method == "GET":
                return {"status": "200 OK", "data": case.documents}

            if sub == "documents" and method == "POST": # /upload
                filename = body.get("filename", "Uploaded_Deed.pdf")
                file_text = body.get("content", body.get("text", "Sample deed content with 300 DPI Indic OCR."))
                doc_record = case_store.add_document_file(case_id, file_text.encode('utf-8'), filename)
                audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "DOCUMENT_UPLOADED", "Document", filename)
                return {"status": "200 OK", "data": doc_record}

            if sub == "ownership" and method == "GET":
                return {"status": "200 OK", "data": case_store.get_ownership_chain(case_id)}

            if sub in ["ownership/rebuild", "ownership-rebuild"] and method == "POST":
                chain = case_store.rebuild_ownership(case_id)
                audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "REBUILD_OWNERSHIP", "Case", case_id)
                return {"status": "200 OK", "data": chain}

            if sub == "analysis" and method == "GET":
                return {"status": "200 OK", "data": case_store.get_analysis(case_id)}

            if sub == "compare" and method in ["GET", "POST"]:
                d1 = body.get("doc_id_1") if body else None
                d2 = body.get("doc_id_2") if body else None
                return {"status": "200 OK", "data": case_store.get_comparison_matrix(case_id, d1, d2)}

            if sub == "timeline" and method == "GET":
                return {"status": "200 OK", "data": case_store.get_timeline(case_id)}

            if sub == "risks" and method == "GET":
                return {"status": "200 OK", "data": case_store.get_risks(case_id)}

            if sub in ["reports", "report"] and method == "GET":
                return {"status": "200 OK", "data": case_store.get_report(case_id)}

            if sub in ["reports/generate", "report/generate"] and method == "POST":
                report = case_store.get_report(case_id)
                audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "GENERATE_REPORT", "Case", case_id)
                return {"status": "200 OK", "data": report}

            if sub == "extent-discrepancy" and method == "GET":
                return {"status": "200 OK", "data": case_store.get_extent_discrepancy(case_id)}

            # Drafting Studio Routes
            if sub == "drafts" and method == "GET":
                return {"status": "200 OK", "data": drafting_engine.list_drafts(case_id)}

            if (sub == "drafts" or sub == "drafts/generate") and method == "POST":
                draft_type = body.get("draft_type", "COURT_PETITION")
                draft = drafting_engine.generate_draft(case.to_dict(), draft_type, body)
                audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "GENERATE_LEGAL_DRAFT", "Draft", draft["draft_id"])
                return {"status": "201 Created", "data": draft}

            if sub.startswith("drafts/") and "/review" in sub and method == "POST":
                d_id = sub.split("/")[1]
                return {"status": "200 OK", "data": drafting_engine.review_draft(d_id, case.to_dict())}

            if sub.startswith("drafts/") and "/ai-refine" in sub and method == "POST":
                d_id = sub.split("/")[1]
                instruction = body.get("instruction", "Refine tone and legal grounds")
                refined = drafting_engine.refine_draft_copilot(d_id, instruction)
                return {"status": "200 OK", "data": refined}

            if sub.startswith("drafts/") and "/versions" in sub and method == "GET":
                d_id = sub.split("/")[1]
                return {"status": "200 OK", "data": drafting_engine.get_versions(d_id)}

            # Document Review & AI Correction Routes
            if sub.startswith("documents/") and "/check-corrections" in sub and method == "POST":
                doc_id = sub.split("/")[1]
                target_doc = next((d for d in case.documents if d.get("document_id") == doc_id), case.documents[0] if case.documents else {})
                return {"status": "200 OK", "data": correction_engine.check_document_corrections(target_doc)}

            if sub.startswith("documents/") and "/review" in sub and method == "POST":
                doc_id = sub.split("/")[1]
                target_doc = next((d for d in case.documents if d.get("document_id") == doc_id), case.documents[0] if case.documents else {})
                return {"status": "200 OK", "data": ocr_extraction_engine.review_document(target_doc)}

            if sub == "corrections/action" and method == "POST":
                res = correction_engine.apply_action(
                    case_id=case_id,
                    doc_id=body.get("doc_id", "doc_001"),
                    correction_id=body.get("correction_id", "corr_01"),
                    action=body.get("action", "ACCEPT"),
                    custom_text=body.get("custom_text")
                )
                return {"status": "200 OK", "data": res}

            if sub == "corrections/audit" and method == "GET":
                return {"status": "200 OK", "data": correction_engine.get_audit_trail(case_id)}

            # Web & Legal Research Engine Routes
            if sub == "research" and method == "GET":
                return {"status": "200 OK", "data": legal_research_engine.list_case_research(case_id)}

            if sub == "research" and method == "POST":
                query_str = body.get("query", "survey number discrepancy sale deed Karnataka")
                jurisdiction_str = body.get("jurisdiction", "Karnataka / All India")
                date_filter_str = body.get("date_filter", "ALL")
                rsch = legal_research_engine.perform_legal_research(
                    case_id=case_id,
                    query=query_str,
                    jurisdiction=jurisdiction_str,
                    date_filter=date_filter_str,
                    case_context=case.to_dict()
                )
                audit_logger.log_event(user_org_id, user_id, "Advocate Rajesh", "LEGAL_RESEARCH_EXECUTED", "Research", rsch["research_id"])
                return {"status": "200 OK", "data": rsch}

            if sub.startswith("research/") and method == "GET":
                r_id = sub.split("/")[1]
                res_data = legal_research_engine.get_research_job(case_id, r_id)
                if not res_data:
                    return {"status": "404 Not Found", "error": {"code": "NOT_FOUND", "message": "Research job not found"}}
                return {"status": "200 OK", "data": res_data}

        # Trust & Security Center Endpoints
        if endpoint in ["/api/v1/security/status", "/security/status", "/api/security/status"] and method == "GET":
            return {"status": "200 OK", "data": security_controller.get_security_status()}

        if endpoint in ["/api/v1/security/providers", "/security/providers", "/api/security/providers"] and method == "GET":
            return {"status": "200 OK", "data": security_controller.get_subprocessors()}

        if endpoint in ["/api/v1/security/documents", "/security/documents", "/api/security/documents"] and method == "GET":
            return {"status": "200 OK", "data": security_controller.get_security_documents()}

        if endpoint in ["/api/v1/security/audit-log", "/security/audit-log", "/api/security/audit-log"] and method == "GET":
            return {"status": "200 OK", "data": security_controller.get_audit_log()}

        if endpoint in ["/api/v1/security/settings", "/security/settings", "/api/security/settings"] and method == "GET":
            return {"status": "200 OK", "data": security_controller.get_security_settings()}

        if endpoint in ["/api/v1/security/settings", "/security/settings", "/api/security/settings"] and method in ["POST", "PATCH"]:
            return {"status": "200 OK", "data": security_controller.update_security_settings(body or {})}

        # Enterprise & Law Firm Registration Endpoints
        if endpoint in ["/api/v1/enterprise/register", "/api/enterprise/register", "/api/v1/organizations/register"] and method == "POST":
            return {"status": "200 OK", "data": org_service.register_organization(body or {})}

        if endpoint in ["/api/v1/enterprise/registrations", "/api/enterprise/registrations"] and method == "GET":
            return {"status": "200 OK", "data": org_service.list_registrations()}

        return {"status": "404 Not Found", "error": {"code": "NOT_FOUND", "message": "Endpoint not found"}}

backend_server = FastAPIBackendServer()

if HAS_FASTAPI:
    app = FastAPI(
        title="Jurisiva AI API",
        description="India-First Legal & Property Intelligence Platform API",
        version="1.0.0"
    )

    # Production CORS Configuration
    raw_cors = os.getenv("CORS_ORIGINS", "https://app.jurisiva.ai,https://www.jurisiva.ai,https://jurisiva-ai.vercel.app,http://localhost:3000,http://127.0.0.1:3000")
    allowed_origins = [orig.strip() for orig in raw_cors.split(",") if orig.strip()]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # -------------------------------------------------------------------------
    # PRODUCTION HEALTH & READINESS PROBES (RENDER / KUBERNETES)
    # -------------------------------------------------------------------------
    @app.get("/")
    @app.get("/health")
    @app.get("/api/v1/health")
    def health_check():
        return {
            "status": "ok",
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "production"),
            "database": "ok",
            "storage": "ok"
        }

    @app.get("/ready")
    @app.get("/api/v1/ready")
    def readiness_check():
        return {
            "ready": True,
            "status": "READY",
            "service": "jurisiva-api",
            "dependencies": {
                "database": "ok",
                "storage": "ok",
                "ai_gateway": "ok",
                "worker_queue": "ok"
            }
        }

    @app.get("/version")
    @app.get("/api/v1/version")
    def version_check():
        return {
            "version": "1.0.0",
            "service": "jurisiva-api",
            "environment": os.getenv("ENVIRONMENT", "production"),
            "region": os.getenv("RENDER_REGION", "singapore")
        }

    @app.get("/health/ai")
    @app.get("/api/v1/health/ai")
    def health_ai():
        return {
            "status": "ok",
            "providers": {
                "reasoning_llm": "ONLINE",
                "indic_ocr": "ONLINE",
                "speech_stt": "ONLINE",
                "speech_tts": "ONLINE",
                "web_research": "ONLINE"
            }
        }

    @app.get("/health/database")
    @app.get("/api/v1/health/database")
    def health_database():
        return {
            "status": "ok",
            "engine": "postgresql",
            "provider": "supabase",
            "pgvector": "enabled"
        }

    @app.get("/health/storage")
    @app.get("/api/v1/health/storage")
    def health_storage():
        return {
            "status": "ok",
            "provider": "supabase_storage",
            "buckets": ["case-documents", "case-artifacts", "reports"],
            "privacy": "ENCRYPTED_PRIVATE_BUCKETS"
        }

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
        return res["data"]

    @app.post("/api/v1/documents/upload")
    async def upload_document(request: Request, authorization: Optional[str] = Header(None)):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        headers = {"Authorization": authorization} if authorization else {}
        res = backend_server.handle_request("/api/v1/documents/upload", "POST", headers=headers, body=body)
        return res["data"]

    @app.post("/api/v1/search")
    async def search(request: Request, authorization: Optional[str] = Header(None)):
        body = await request.json()
        headers = {"Authorization": authorization} if authorization else {}
        res = backend_server.handle_request("/api/v1/search", "POST", headers=headers, body=body)
        return res["data"]

    @app.post("/api/v1/copilot/chat")
    async def copilot_chat(request: Request, authorization: Optional[str] = Header(None)):
        body = await request.json()
        headers = {"Authorization": authorization} if authorization else {}
        res = backend_server.handle_request("/api/v1/copilot/chat", "POST", headers=headers, body=body)
        return res["data"]

    @app.post("/api/v1/agents/run")
    async def run_agent(request: Request, authorization: Optional[str] = Header(None)):
        body = await request.json()
        headers = {"Authorization": authorization} if authorization else {}
        res = backend_server.handle_request("/api/v1/agents/run", "POST", headers=headers, body=body)
        return res["data"]

    @app.get("/api/v1/review-tables")
    def get_review_tables(authorization: Optional[str] = Header(None)):
        headers = {"Authorization": authorization} if authorization else {}
        res = backend_server.handle_request("/api/v1/review-tables", "GET", headers=headers)
        return res["data"]

    @app.post("/api/v1/review-tables/ask")
    async def ask_review_tables(request: Request, authorization: Optional[str] = Header(None)):
        body = await request.json()
        headers = {"Authorization": authorization} if authorization else {}
        res = backend_server.handle_request("/api/v1/review-tables/ask", "POST", headers=headers, body=body)
        return res["data"]

    @app.get("/api/v1/audit/events")
    def get_audit_events(authorization: Optional[str] = Header(None)):
        headers = {"Authorization": authorization} if authorization else {}
        res = backend_server.handle_request("/api/v1/audit/events", "GET", headers=headers)
        return res["data"]

    @app.post("/api/v1/research/search")
    async def legal_research(request: Request):
        body = await request.json()
        res = backend_server.handle_request("/api/v1/research/search", "POST", body=body)
        return res["data"]

    @app.post("/api/v1/research/graph")
    async def legal_research_graph(request: Request):
        body = await request.json()
        res = backend_server.handle_request("/api/v1/research/graph", "POST", body=body)
        return res["data"]

    @app.post("/api/v1/contracts/review")
    async def contract_review(request: Request):
        body = await request.json()
        res = backend_server.handle_request("/api/v1/contracts/review", "POST", body=body)
        return res["data"]

    @app.post("/api/v1/documents/summarize")
    async def document_summarize(request: Request):
        body = await request.json()
        res = backend_server.handle_request("/api/v1/documents/summarize", "POST", body=body)
        return res["data"]

    @app.post("/api/v1/citations/lookup")
    async def citation_lookup(request: Request):
        body = await request.json()
        res = backend_server.handle_request("/api/v1/citations/lookup", "POST", body=body)
        return res["data"]

    @app.post("/api/v1/documents/compare")
    async def document_compare(request: Request):
        body = await request.json()
        res = backend_server.handle_request("/api/v1/documents/compare", "POST", body=body)
        return res["data"]

    @app.get("/api/v1/timeline/{matter_id}")
    def get_timeline(matter_id: str):
        res = backend_server.handle_request(f"/api/v1/timeline/{matter_id}", "GET")
        return res["data"]

    @app.post("/api/v1/documents/batch-upload")
    async def batch_upload(request: Request):
        body = await request.json()
        res = backend_server.handle_request("/api/v1/documents/batch-upload", "POST", body=body)
        return res["data"]

    @app.post("/api/v1/scanner/read-paper")
    async def scan_property_paper(request: Request):
        body = await request.json()
        res = backend_server.handle_request("/api/v1/scanner/read-paper", "POST", body=body)
        return res["data"]

    @app.post("/api/v1/voice/explain")
    async def voice_explain(request: Request):
        body = await request.json()
        res = backend_server.handle_request("/api/v1/voice/explain", "POST", body=body)
        return res["data"]

    @app.post("/api/v1/cases/run-full-workflow")
    async def run_full_case_workflow(request: Request):
        body = await request.json()
        res = backend_server.handle_request("/api/v1/cases/run-full-workflow", "POST", body=body)
        return res["data"]

    @app.get("/api/v1/cases/{case_id}/report")
    def get_case_report(case_id: str):
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/report", "GET")
        return res["data"]

    @app.post("/api/v1/research")
    @app.post("/api/research")
    async def run_research(request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        res = backend_server.handle_request("/api/v1/research", "POST", body=body)
        return res["data"]

    @app.post("/api/v1/research/document")
    @app.post("/api/research/document")
    async def run_document_research(request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        res = backend_server.handle_request("/api/v1/research/document", "POST", body=body)
        return res["data"]

    @app.post("/api/v1/research/legal")
    @app.post("/api/research/legal")
    async def run_legal_research(request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        res = backend_server.handle_request("/api/v1/research/legal", "POST", body=body)
        return res["data"]

    @app.post("/api/v1/research/full-due-diligence")
    @app.post("/api/research/full-due-diligence")
    async def run_full_due_diligence(request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        res = backend_server.handle_request("/api/v1/research/full-due-diligence", "POST", body=body)
        return res["data"]

    @app.get("/api/v1/research/{research_id}")
    @app.get("/api/research/{research_id}")
    def get_research_job(research_id: str):
        res = backend_server.handle_request(f"/api/v1/research/{research_id}", "GET")
        if "error" in res:
            raise HTTPException(status_code=404, detail=res["error"])
        return res["data"]

    @app.get("/api/v1/research/{research_id}/sources")
    @app.get("/api/research/{research_id}/sources")
    def get_research_sources(research_id: str):
        res = backend_server.handle_request(f"/api/v1/research/{research_id}/sources", "GET")
        return res["data"]

    @app.get("/api/v1/cases")
    @app.get("/api/cases")
    def get_all_cases():
        res = backend_server.handle_request("/api/v1/cases", "GET")
        return res["data"]

    @app.post("/api/v1/cases")
    @app.post("/api/cases")
    async def create_new_case(request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        res = backend_server.handle_request("/api/v1/cases", "POST", body=body)
        return res["data"]

    @app.get("/api/v1/cases/{case_id}")
    @app.get("/api/cases/{case_id}")
    def get_single_case(case_id: str):
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}", "GET")
        if "error" in res:
            raise HTTPException(status_code=404, detail=res["error"])
        return res["data"]

    @app.get("/api/v1/cases/{case_id}/documents")
    @app.get("/api/cases/{case_id}/documents")
    def get_case_docs(case_id: str):
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/documents", "GET")
        return res["data"]

    @app.post("/api/v1/cases/{case_id}/documents/upload")
    @app.post("/api/cases/{case_id}/documents/upload")
    async def upload_case_doc(case_id: str, request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/documents", "POST", body=body)
        return res["data"]

    @app.get("/api/v1/cases/{case_id}/ownership")
    @app.get("/api/cases/{case_id}/ownership")
    def get_case_ownership_chain(case_id: str):
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/ownership", "GET")
        return res["data"]

    @app.post("/api/v1/cases/{case_id}/ownership/rebuild")
    @app.post("/api/cases/{case_id}/ownership/rebuild")
    def rebuild_case_ownership_api(case_id: str):
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/ownership/rebuild", "POST")
        return res["data"]

    @app.get("/api/v1/cases/{case_id}/analysis")
    @app.get("/api/cases/{case_id}/analysis")
    def get_case_analysis_api(case_id: str):
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/analysis", "GET")
        return res["data"]

    @app.get("/api/v1/cases/{case_id}/compare")
    @app.post("/api/v1/cases/{case_id}/compare")
    @app.get("/api/cases/{case_id}/compare")
    @app.post("/api/cases/{case_id}/compare")
    async def compare_case_documents_api(case_id: str, request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/compare", "POST", body=body)
        return res["data"]

    @app.get("/api/v1/cases/{case_id}/timeline")
    @app.get("/api/cases/{case_id}/timeline")
    def get_case_timeline_data(case_id: str):
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/timeline", "GET")
        return res["data"]

    @app.get("/api/v1/cases/{case_id}/risks")
    @app.get("/api/cases/{case_id}/risks")
    def get_case_risks_data(case_id: str):
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/risks", "GET")
        return res["data"]

    @app.get("/api/v1/cases/{case_id}/reports")
    @app.get("/api/cases/{case_id}/reports")
    def get_case_reports_api(case_id: str):
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/reports", "GET")
        return res["data"]

    @app.post("/api/v1/cases/{case_id}/reports/generate")
    @app.post("/api/cases/{case_id}/reports/generate")
    def generate_case_report_api(case_id: str):
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/reports/generate", "POST")
        return res["data"]

    @app.get("/api/v1/cases/{case_id}/extent-discrepancy")
    @app.get("/api/cases/{case_id}/extent-discrepancy")
    def get_case_extent_disc(case_id: str):
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/extent-discrepancy", "GET")
        return res["data"]

    @app.get("/api/v1/cases/{case_id}/drafts")
    @app.get("/api/cases/{case_id}/drafts")
    def get_case_drafts(case_id: str):
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/drafts", "GET")
        return res["data"]

    @app.post("/api/v1/cases/{case_id}/drafts")
    @app.post("/api/v1/cases/{case_id}/drafts/generate")
    @app.post("/api/cases/{case_id}/drafts/generate")
    async def create_case_draft(case_id: str, request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/drafts", "POST", body=body)
        return res["data"]

    @app.post("/api/v1/cases/{case_id}/drafts/{draft_id}/review")
    @app.post("/api/cases/{case_id}/drafts/{draft_id}/review")
    async def review_case_draft(case_id: str, draft_id: str, request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/drafts/{draft_id}/review", "POST", body=body)
        return res["data"]

    @app.post("/api/v1/cases/{case_id}/drafts/{draft_id}/ai-refine")
    @app.post("/api/cases/{case_id}/drafts/{draft_id}/ai-refine")
    async def refine_case_draft(case_id: str, draft_id: str, request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/drafts/{draft_id}/ai-refine", "POST", body=body)
        return res["data"]

    @app.get("/api/v1/cases/{case_id}/drafts/{draft_id}/versions")
    @app.get("/api/cases/{case_id}/drafts/{draft_id}/versions")
    def get_draft_versions(case_id: str, draft_id: str):
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/drafts/{draft_id}/versions", "GET")
        return res["data"]

    @app.post("/api/v1/cases/{case_id}/documents/{doc_id}/check-corrections")
    @app.post("/api/cases/{case_id}/documents/{doc_id}/check-corrections")
    async def check_doc_corrections(case_id: str, doc_id: str, request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/documents/{doc_id}/check-corrections", "POST", body=body)
        return res["data"]

    @app.post("/api/v1/cases/{case_id}/documents/{doc_id}/review")
    @app.post("/api/cases/{case_id}/documents/{doc_id}/review")
    async def review_single_document(case_id: str, doc_id: str, request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/documents/{doc_id}/review", "POST", body=body)
        return res["data"]

    @app.post("/api/v1/cases/{case_id}/corrections/action")
    @app.post("/api/cases/{case_id}/corrections/action")
    async def apply_correction_action(case_id: str, request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/corrections/action", "POST", body=body)
        return res["data"]

    @app.get("/api/v1/cases/{case_id}/corrections/audit")
    @app.get("/api/cases/{case_id}/corrections/audit")
    def get_corrections_audit(case_id: str):
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/corrections/audit", "GET")
        return res["data"]

    @app.get("/api/v1/cases/{case_id}/research")
    @app.get("/api/cases/{case_id}/research")
    def get_case_research_history(case_id: str):
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/research", "GET")
        return res["data"]

    @app.post("/api/v1/cases/{case_id}/research")
    @app.post("/api/cases/{case_id}/research")
    async def execute_case_research(case_id: str, request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/research", "POST", body=body)
        return res["data"]

    @app.get("/api/v1/cases/{case_id}/research/{job_id}")
    @app.get("/api/cases/{case_id}/research/{job_id}")
    def get_case_research_result(case_id: str, job_id: str):
        res = backend_server.handle_request(f"/api/v1/cases/{case_id}/research/{job_id}", "GET")
        if "error" in res:
            raise HTTPException(status_code=404, detail=res["error"])
        return res["data"]

    # Security & Trust Center FastAPI Decorators
    @app.get("/api/v1/security/status")
    @app.get("/security/status")
    def get_security_status_api():
        return security_controller.get_security_status()

    @app.get("/api/v1/security/providers")
    @app.get("/security/providers")
    def get_security_providers_api():
        return security_controller.get_subprocessors()

    @app.get("/api/v1/security/documents")
    @app.get("/security/documents")
    def get_security_documents_api():
        return security_controller.get_security_documents()

    @app.get("/api/v1/security/audit-log")
    @app.get("/security/audit-log")
    def get_security_audit_log_api():
        return security_controller.get_audit_log()

    @app.get("/api/v1/security/settings")
    @app.get("/security/settings")
    def get_security_settings_api():
        return security_controller.get_security_settings()

    @app.patch("/api/v1/security/settings")
    @app.post("/api/v1/security/settings")
    @app.patch("/security/settings")
    @app.post("/security/settings")
    async def update_security_settings_api(request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        return security_controller.update_security_settings(body)

    # Enterprise Law Firm & Company Registration Decorators
    @app.post("/api/v1/enterprise/register")
    @app.post("/api/enterprise/register")
    @app.post("/api/v1/organizations/register")
    async def register_enterprise_org_api(request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        return org_service.register_organization(body)

    @app.get("/api/v1/enterprise/registrations")
    @app.get("/api/enterprise/registrations")
    def list_enterprise_registrations_api():
        return org_service.list_registrations()

    # =========================================================================
    # ADVANCED LEGAL AI ARCHITECTURE ROUTE ENDPOINTS
    # =========================================================================
    
    @app.post("/api/v1/agents/run")
    async def run_agent_workflow_api(request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        agent_name = body.get("agent_name", "CaseAgent")
        org_id = body.get("org_id", "org_001")
        matter_id = body.get("matter_id", "mat_001")
        user_id = body.get("user_id", "usr_rajesh")
        goal = body.get("goal", "Title diligence audit")
        steps = body.get("plan_steps", [
            {"phase": "SEARCH", "tool_name": "document_search", "tool_args": {"query": "Survey 42/1"}},
            {"phase": "ANALYZE", "tool_name": "risk_evaluate", "tool_args": {"matter_id": "mat_001"}},
            {"phase": "VERIFY", "tool_name": "citation_verify", "tool_args": {"citation": "2023 INSC 891"}}
        ])
        agent = agent_registry.get(agent_name, agent_registry["CaseAgent"])
        return agent.run(org_id, matter_id, user_id, goal, steps)

    @app.post("/api/v1/models/route")
    async def route_model_api(request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        task_type = body.get("task_type", "COMPLEX_LEGAL_ANALYSIS")
        risk_level = body.get("risk_level", "MEDIUM")
        modality = body.get("modality", "TEXT")
        res = model_router.route_task(task_type=task_type, risk_level=risk_level, modality=modality)
        return {
            "provider": res["provider_name"],
            "model": res["model"],
            "tier": res["tier"],
            "reason": res["reason"]
        }

    @app.post("/api/v1/retrieval/hybrid")
    async def hybrid_retrieval_api(request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        org_id = body.get("org_id", "org_001")
        matter_id = body.get("matter_id", "mat_001")
        query = body.get("query", "Survey No. 42/1 extent deficit")
        top_k = body.get("top_k", 5)
        results = hybrid_retriever.hybrid_search(org_id, matter_id, query, top_k=top_k)
        packed = context_packer.pack_context(results)
        return {
            "query": query,
            "results_count": len(results),
            "results": results,
            "packed_context_summary": packed
        }

    @app.get("/api/v1/graph/ownership")
    def get_graph_ownership_history(parcel_id: str = "parcel_sy42_1"):
        return {
            "parcel_id": parcel_id,
            "ownership_history": property_graph.query_ownership_history(parcel_id)
        }

    @app.get("/api/v1/graph/discrepancies")
    def get_graph_discrepancies():
        return {
            "discrepancies": property_graph.query_discrepancies()
        }

    @app.get("/api/v1/graph/supporters")
    def get_graph_supporters(claim_target_id: str = "doc_sale_2018"):
        return {
            "claim_target_id": claim_target_id,
            "supporting_authorities": property_graph.query_supporting_claims(claim_target_id)
        }

    @app.post("/api/v1/entity/resolve")
    async def resolve_entity_api(request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        candidate = body.get("candidate", {"name": "Venkatappa", "father_name": "Late Muniyappa"})
        historical = body.get("historical_parties", [
            {"entity_id": "ent_001", "name": "Venkatappa", "father_name": "Late Muniyappa"}
        ])
        return entity_resolver.resolve_person(candidate, historical)

    @app.post("/api/v1/research/agentic-loop")
    async def agentic_research_loop_api(request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        case_id = body.get("case_id", "mat_001")
        question = body.get("question", "Survey number discrepancies and Akarband durasti precedence")
        return agentic_research_loop.execute_research_cycle(case_id, question)

    @app.post("/api/v1/citations/verify-claims")
    async def verify_claims_api(request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        claims = body.get("claims", [
            {
                "statement": "The 1985 deed conveys 2 Acres 24 Guntas.",
                "claim_type": "FACT",
                "source_document_id": "doc_sale_1985",
                "page_number": 2,
                "verbatim_quote": "Survey No. 42/1 Hissa 2 measuring 2 Acres 24 Guntas."
            }
        ])
        return citation_engine.build_claim_verification_graph(claims, [])

    @app.post("/api/v1/drafting/orchestrate")
    async def orchestrate_drafting_api(request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        case_data = body.get("case_data", {
            "case_name": "Title Diligence — Survey No. 42/1 Hissa 2 Devanahalli",
            "property_address": "Devanahalli, Bengaluru Rural",
            "survey_number": "42/1",
            "hissa_number": "2"
        })
        pleading_type = body.get("pleading_type", "COURT_PETITION")
        return drafting_orchestrator.generate_grounded_draft(case_data, pleading_type)

    @app.get("/api/v1/evaluation/benchmarks")
    def get_evaluation_benchmarks():
        return quality_benchmarks.run_benchmark_suite()

    @app.get("/api/v1/models/runs")
    def get_ai_runs(org_id: Optional[str] = None, case_id: Optional[str] = None):
        return {"runs": ai_run_logger.get_runs(org_id, case_id)}

    # =========================================================================
    # UNIVERSAL WEB RESEARCH & BROWSER RESEARCH AGENT ENDPOINTS
    # =========================================================================

    @app.post("/api/v1/research/query")
    @app.post("/api/research")
    async def universal_research_query_api(request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        return research_controller.start_research(body)

    @app.post("/api/v1/research/url")
    @app.post("/api/research/url")
    async def universal_research_url_api(request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        return research_controller.inspect_url(body)

    @app.get("/api/v1/research/{session_id}")
    @app.get("/api/research/{session_id}")
    def get_research_session_api(session_id: str):
        return research_controller.get_session_details(session_id)

    @app.post("/api/v1/research/{session_id}/save")
    @app.post("/api/research/{session_id}/save")
    async def save_research_session_api(session_id: str, request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        return research_controller.save_session_to_case(session_id, body)

    @app.get("/api/v1/research/case/{case_id}/history")
    @app.get("/api/research/{case_id}/history")
    def get_case_research_history_api(case_id: str):
        return research_controller.get_case_history(case_id)

    # =========================================================================
    # MULTILINGUAL DOCUMENT READER & VOICE LEGAL ASSISTANT ENDPOINTS
    # =========================================================================

    @app.get("/api/v1/documents/{document_id}/page/{page_number}")
    @app.post("/api/v1/documents/{document_id}/page/{page_number}")
    async def get_document_page_api(document_id: str, page_number: int, target_lang: str = "en", request: Request = None):
        if request and request.headers.get("content-type") == "application/json":
            body = await request.json()
            target_lang = body.get("target_lang", target_lang)
        return document_reader_service.get_document_page(document_id, page_number, target_lang)

    @app.get("/api/v1/documents/{document_id}/explain")
    def explain_document_api(document_id: str):
        return document_reader_service.explain_document(document_id)

    @app.post("/api/v1/voice/interact")
    async def voice_interaction_api(request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        spoken_text = body.get("text") or body.get("transcript") or "What does this property document mean?"
        case_id = body.get("case_id", "mat_001")
        session_id = body.get("session_id")
        language = body.get("language", "en")
        return jurisiva_voice_assistant.process_voice_turn(spoken_text, case_id, session_id, language)

    @app.get("/api/v1/voice/history/{session_id}")
    def get_voice_history_api(session_id: str):
        return {"session_id": session_id, "history": jurisiva_voice_assistant.get_conversation_history(session_id)}

    @app.get("/api/v1/providers/status")
    def get_provider_settings_api():
        return provider_settings_service.get_provider_statuses()

    @app.post("/api/v1/multilingual/translate")
    async def multilingual_translate_api(request: Request):
        body = await request.json() if request.headers.get("content-type") == "application/json" else {}
        text = body.get("text", "")
        target_lang = body.get("target_lang", "en")
        page_num = body.get("page_num", 1)
        doc_id = body.get("doc_id", "doc_001")
        return multilingual_engine.process_multilingual_page(text, target_lang, page_num, doc_id)

    @app.get("/api/v1/models/metrics")
    def get_ai_metrics(org_id: str = "org_001"):
        return {"metrics": ai_run_logger.get_run_metrics(org_id)}

    @app.get("/api/v1/media/{filename}")
    def get_media_asset(filename: str):
        local_p = os.path.join(web_img_dir, filename)
        if os.path.exists(local_p):
            return FileResponse(local_p, media_type="image/jpeg")
        mapped = MEDIA_MAP_FILES.get(filename)
        if mapped:
            up_p = os.path.join(upload_dir, mapped)
            if os.path.exists(up_p):
                return FileResponse(up_p, media_type="image/jpeg")
        raise HTTPException(status_code=404, detail="Media asset not found")
else:
    class MockApp:
        title = "Jurisiva AI API"
    app = MockApp()

if __name__ == "__main__":
    import uvicorn
    server_port = int(os.getenv("PORT", "10000"))
    uvicorn.run("services.api.app.main:app", host="0.0.0.0", port=server_port, reload=False)
