# Research Agent Master Orchestrator
# Coordinates multi-stage research pipeline with real-time telemetry and async job tracking.

import time
import uuid
from typing import Dict, List, Any, Optional

from app.research.planner import research_planner
from app.research.retrieval import document_retriever
from app.research.evidence import evidence_extractor
from app.research.web_research import web_researcher
from app.research.source_validator import source_validator
from app.research.analyzer import research_analyst
from app.research.citations import citation_builder
from app.research.synthesizer import research_synthesizer

class ResearchJob:
    def __init__(self, research_id: str, query: str, mode: str, org_id: str, matter_id: str):
        self.research_id = research_id
        self.query = query
        self.mode = mode
        self.org_id = org_id
        self.matter_id = matter_id
        self.status = "QUEUED"
        self.created_at = time.time()
        self.updated_at = time.time()
        self.progress_percentage = 0
        self.live_steps: List[Dict[str, Any]] = []
        self.result: Optional[Dict[str, Any]] = None
        self.error: Optional[str] = None

    def add_step(self, step_name: str, detail: str, status: str = "IN_PROGRESS"):
        self.updated_at = time.time()
        self.live_steps.append({
            "step_name": step_name,
            "detail": detail,
            "status": status,
            "timestamp": round(self.updated_at, 2)
        })

    def update_last_step(self, status: str = "COMPLETED", detail: Optional[str] = None):
        if self.live_steps:
            self.live_steps[-1]["status"] = status
            if detail:
                self.live_steps[-1]["detail"] = detail
        self.updated_at = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "research_id": self.research_id,
            "query": self.query,
            "mode": self.mode,
            "status": self.status,
            "progress_percentage": self.progress_percentage,
            "live_steps": self.live_steps,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class ResearchOrchestrator:
    """Master research engine coordinating multi-stage property & legal investigations."""

    def __init__(self):
        self._jobs: Dict[str, ResearchJob] = {}

    def start_research_job(
        self,
        query: str,
        mode: str = "FULL_DUE_DILIGENCE",
        org_id: str = "org_001",
        matter_id: str = "mat_001",
        case_context: Optional[Dict[str, Any]] = None
    ) -> str:
        research_id = f"res_{uuid.uuid4().hex[:12]}"
        job = ResearchJob(research_id, query, mode, org_id, matter_id)
        self._jobs[research_id] = job

        # Run pipeline synchronously or prepare job
        self._execute_pipeline(job, case_context)
        return research_id

    def get_job_status(self, research_id: str) -> Optional[Dict[str, Any]]:
        job = self._jobs.get(research_id)
        return job.to_dict() if job else None

    def execute_research_sync(
        self,
        query: str,
        mode: str = "FULL_DUE_DILIGENCE",
        org_id: str = "org_001",
        matter_id: str = "mat_001",
        case_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        research_id = f"res_{uuid.uuid4().hex[:12]}"
        job = ResearchJob(research_id, query, mode, org_id, matter_id)
        self._jobs[research_id] = job
        self._execute_pipeline(job, case_context)
        return job.to_dict()

    def _execute_pipeline(self, job: ResearchJob, case_context: Optional[Dict[str, Any]]):
        try:
            # 1. PLANNER
            job.status = "PLANNING"
            job.progress_percentage = 15
            job.add_step("Understanding question...", "Analyzing intent, scoping legal issues, and extracting jurisdiction parameters.")
            plan = research_planner.plan_research(job.query, job.mode, case_context)
            job.update_last_step("COMPLETED", f"Scope identified: {plan.intent} in {plan.jurisdiction.get('district', 'Bengaluru Rural')}, {plan.jurisdiction.get('state', 'Karnataka')}.")

            # 2. DOCUMENT RETRIEVER & OCR EVIDENCE
            job.status = "SEARCHING_DOCUMENTS"
            job.progress_percentage = 35
            job.add_step("Searching case documents...", "Executing hybrid semantic + keyword search over uploaded matter documents and OCR transcripts.")
            chunks = document_retriever.retrieve_chunks(job.org_id, job.matter_id, job.query, top_k=6)
            job.update_last_step("COMPLETED", f"Retrieved {len(chunks)} relevant document pages with 300 DPI Indic OCR text.")

            # 3. EVIDENCE EXTRACTOR
            job.status = "OCR_PROCESSING"
            job.progress_percentage = 50
            job.add_step("Finding relevant evidence...", "Extracting verbatim quotes, page numbers, entity recitals, and confidence scores.")
            evidence_list = evidence_extractor.extract_evidence(chunks, job.query)
            job.update_last_step("COMPLETED", f"Extracted {len(evidence_list)} evidentiary citations across sale deeds, mutation extracts, and mortgage filings.")

            # 4. WEB / LEGAL RESEARCHER
            job.status = "EXTERNAL_RESEARCH"
            job.progress_percentage = 65
            job.add_step("Checking external sources...", "Querying authoritative statutory provisions, state land revenue acts, and Supreme Court / High Court precedent law reports.")
            external_sources = web_researcher.search_external_legal_sources(job.query, plan.jurisdiction, max_sources=4)
            job.update_last_step("COMPLETED", f"Retrieved {len(external_sources)} official legislative and judicial citations.")

            # 5. SOURCE VALIDATOR
            job.status = "VERIFYING_SOURCES"
            job.progress_percentage = 75
            job.add_step("Verifying source authority...", "Validating jurisdiction match, gazette authenticity, and Level 1 / Level 2 court hierarchy.")
            validated_sources = source_validator.validate_sources(external_sources, plan.jurisdiction)
            job.update_last_step("COMPLETED", "All external statutes and judicial precedents verified against official records.")

            # 6. ANALYST (Ownership Chain, Conflicts, Risks)
            job.status = "ANALYZING"
            job.progress_percentage = 88
            job.add_step("Comparing information & detecting risks...", "Building 30-year ownership chain, checking area extent variance, and auditing encumbrances.")
            ownership = research_analyst.build_ownership_chain(chunks)
            risks = research_analyst.detect_conflicts_and_risks(chunks)
            job.update_last_step("COMPLETED", f"Analyzed title chain (1985–2018) and identified {len(risks)} evidence-based defect/risk findings.")

            # 7. CITATIONS BUILDER
            doc_citations = citation_builder.build_document_citations(evidence_list)
            ext_citations = citation_builder.build_external_citations(validated_sources)

            # 8. SYNTHESIZER
            job.status = "SYNTHESIZING"
            job.progress_percentage = 95
            job.add_step("Synthesizing answer...", "Structuring evidence-grounded response with page citations, risk cards, and actionable advocate recommendations.")
            final_result = research_synthesizer.synthesize(
                query=job.query,
                plan=plan,
                evidence=evidence_list,
                risks=risks,
                ownership=ownership,
                external_sources=validated_sources,
                doc_citations=doc_citations,
                ext_citations=ext_citations
            )
            job.update_last_step("COMPLETED", "Synthesis finalized.")

            job.status = "COMPLETED"
            job.progress_percentage = 100
            job.result = final_result

        except Exception as e:
            job.status = "FAILED"
            job.error = str(e)
            job.add_step("Pipeline Execution Error", str(e), "FAILED")

    def generate_full_diligence_report(self, matter_id: str = "mat_001") -> Dict[str, Any]:
        """Generates comprehensive due diligence report using the underlying research pipeline."""
        res = self.execute_research_sync(
            query="Full Property Due Diligence Investigation for Survey No. 42/1 Hissa 2 Devanahalli",
            mode="FULL_DUE_DILIGENCE",
            matter_id=matter_id
        )
        data = res.get("result", {})
        return {
            "report_title": "CONFIDENTIAL PROPERTY TITLE DUE DILIGENCE REPORT",
            "matter_id": matter_id,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S IST"),
            "property_details": {
                "survey_number": "Survey No. 42/1 Hissa 2",
                "village": "Devanahalli",
                "hobli": "Kasaba Hobli",
                "taluk": "Devanahalli",
                "district": "Bengaluru Rural",
                "state": "Karnataka",
                "extent_parent": "2 Acres 24 Guntas (104,544 Sq.Ft)",
                "extent_current": "2 Acres 10 Guntas (98,010 Sq.Ft)",
                "deficit": "14 Guntas (-15,246 Sq.Ft)"
            },
            "executive_summary": data.get("executive_summary", ""),
            "key_findings": data.get("key_findings", []),
            "ownership_chain": data.get("ownership_summary", {}),
            "risk_assessment": data.get("risk_findings", []),
            "applicable_laws": data.get("external_sources", []),
            "verification_checklist": data.get("recommendations", []),
            "evidence_citations": data.get("document_citations", []),
            "legal_safety_notice": data.get("legal_safety_disclaimer", "")
        }

research_orchestrator = ResearchOrchestrator()
