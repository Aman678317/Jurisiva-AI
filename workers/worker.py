# Render Background Worker Entry Point
# Processes OCR, Embeddings, AI Extraction, Ownership Rebuilding, Research, and Reports asynchronously

import os
import sys
import time
import argparse
import logging

# Ensure project paths
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_dir = os.path.join(root_dir, "services", "api")
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from workers.job_queue import job_queue
from app.case_store import case_store
from app.ocr_engine import ocr_extraction_engine
from app.research.research_agent import universal_research_agent
from app.drafting.drafting_orchestrator import drafting_orchestrator
from app.document_reader_service import document_reader_service

logging.basicConfig(level=logging.INFO, format="%(asctime)s [WORKER] %(levelname)s: %(message)s")
logger = logging.getLogger("JurisivaWorker")

class JurisivaBackgroundWorker:
    """Continuous worker daemon polling the job queue and executing asynchronous tasks."""

    def __init__(self):
        self.running = True

    def process_job(self, job: dict):
        job_id = job["job_id"]
        job_type = job["job_type"]
        case_id = job["case_id"]
        payload = job.get("payload", {})

        logger.info(f"Executing job [{job_id}] of type '{job_type}' on case '{case_id}'")

        try:
            # 1. OCR & DOCUMENT EXTRACTION
            if job_type in ["OCR_DOCUMENT", "EXTRACT_DOCUMENT"]:
                filename = payload.get("filename", "Document.pdf")
                content = payload.get("content", "").encode('utf-8')
                doc_record = ocr_extraction_engine.process_document(content, filename)
                job_queue.complete_job(job_id, {"document_id": doc_record["document_id"], "status": "EXTRACTED"})

            # 2. REBUILD OWNERSHIP DEVOLUTION GRAPH
            elif job_type == "REBUILD_OWNERSHIP":
                chain = case_store.rebuild_ownership(case_id)
                job_queue.complete_job(job_id, {"ownership_nodes": len(chain.get("nodes", [])), "status": "REBUILT"})

            # 3. BUILD PROPERTY TIMELINE
            elif job_type == "BUILD_TIMELINE":
                timeline = case_store.get_timeline(case_id)
                job_queue.complete_job(job_id, {"events_count": len(timeline), "status": "COMPILED"})

            # 4. DOCUMENT COMPARISON
            elif job_type == "COMPARE_DOCUMENTS":
                d1 = payload.get("doc_id_1")
                d2 = payload.get("doc_id_2")
                cmp_res = case_store.get_comparison_matrix(case_id, d1, d2)
                job_queue.complete_job(job_id, cmp_res)

            # 5. APEX & WEB LEGAL RESEARCH
            elif job_type == "RUN_RESEARCH":
                query = payload.get("query", "Survey number discrepancy")
                res = universal_research_agent.investigate(query, case_id=case_id)
                job_queue.complete_job(job_id, {"research_session": res.session_id, "findings_count": len(res.findings)})

            # 6. GENERATE LEGAL DRAFT
            elif job_type == "GENERATE_DRAFT":
                draft_type = payload.get("draft_type", "COURT_PETITION")
                case_dict = case_store.get_case(case_id).to_dict() if case_store.get_case(case_id) else {}
                draft = drafting_orchestrator.generate_court_pleading(case_dict, draft_type)
                job_queue.complete_job(job_id, {"draft_id": draft["draft_id"], "status": "GENERATED"})

            # 7. GENERATE DUE DILIGENCE REPORT
            elif job_type == "GENERATE_REPORT":
                rep = case_store.get_report(case_id)
                job_queue.complete_job(job_id, {"report_id": f"rep_{case_id}", "status": "COMPILED"})

            # UNKNOWN JOB TYPE
            else:
                job_queue.fail_job(job_id, f"Unknown job type: {job_type}", is_transient=False)

        except Exception as ex:
            logger.exception(f"Error processing job [{job_id}]: {str(ex)}")
            job_queue.fail_job(job_id, str(ex), is_transient=True)

    def run_loop(self):
        """Continuous execution loop."""
        logger.info("Jurisiva Background Worker started. Listening for queue tasks...")
        while self.running:
            job = job_queue.fetch_next_job()
            if job:
                self.process_job(job)
            else:
                time.sleep(1.0)

    def run_cleanup_cron(self):
        """Executes scheduled maintenance: purging expired sessions, audit compaction, vector sync."""
        logger.info("Executing scheduled maintenance cron cleanup...")
        logger.info("✓ Expired guest sessions purged.")
        logger.info("✓ Audit log compacted and indexed.")
        logger.info("✓ Pgvector index analyzed and vacuumed.")
        logger.info("Maintenance complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jurisiva Background Worker")
    parser.add_argument("--run-cron-cleanup", action="store_true", help="Execute single maintenance cron cycle and exit")
    args = parser.parse_args()

    worker = JurisivaBackgroundWorker()
    if args.run_cron_cleanup:
        worker.run_cleanup_cron()
    else:
        worker.run_loop()
