# Legal & Property Intelligence Workflows Test Suite

import pytest
from app.workflows.property_timeline import timeline_builder
from app.workflows.comparator import document_comparator
from app.workflows.entity_resolution import entity_resolver
from app.workflows.conflict_detector import conflict_detector
from app.workflows.report_builder import report_builder

@pytest.fixture
def sample_deeds():
    return [
        {"document_id": "doc_1985", "execution_date": "1985-08-14", "event_type": "SALE_DEED", "executant": "Venkatappa", "claimant": "Krishnappa", "extent": "2 Acres 24 Guntas", "page_number": 1},
        {"document_id": "doc_2010", "execution_date": "2010-05-20", "event_type": "MORTGAGE_DEED", "executant": "Krishnappa", "claimant": "State Bank of India", "extent": "2 Acres 24 Guntas", "page_number": 1},
        {"document_id": "doc_2018", "execution_date": "2018-11-12", "event_type": "SALE_DEED", "executant": "Krishnappa", "claimant": "Anand Kumar", "extent": "2 Acres 10 Guntas", "page_number": 2}
    ]

def test_workflow_001_property_timeline_builder(sample_deeds):
    timeline = timeline_builder.build_timeline(sample_deeds)
    assert len(timeline["timeline_nodes"]) == 3
    assert len(timeline["title_gaps"]) > 0

def test_workflow_002_document_comparator_diffs():
    text_a = "Clause 1: Consideration is Rs 50,00,000.\nClause 2: Possession transferred."
    text_b = "Clause 1: Consideration is Rs 60,00,000.\nClause 2: Possession transferred."
    diff_res = document_comparator.compare_documents(text_a, text_b)
    assert diff_res["added_count"] == 1
    assert diff_res["removed_count"] == 1
    assert diff_res["unchanged_count"] == 1

def test_workflow_003_cautious_entity_resolution():
    ent1 = {"name": "Rajesh Sharma", "address": "Devanahalli, Bengaluru"}
    ent2 = {"name": "Rajesh Sharma", "address": "Devanahalli, Bengaluru"}
    match_res = entity_resolver.resolve_entity(ent1, ent2)
    assert match_res["status"] == "MATCH"

    ent_ambiguous = {"name": "Rajesh Sharma", "address": "Whitefield, Bengaluru"}
    ambig_res = entity_resolver.resolve_entity(ent1, ent_ambiguous)
    assert ambig_res["status"] == "POSSIBLE_MATCH"
    assert ambig_res["action"] == "FLAG_FOR_REVIEW"

def test_workflow_004_evidence_conflict_detector(sample_deeds):
    conflicts = conflict_detector.detect_conflicts(sample_deeds)
    assert len(conflicts) >= 2

    extent_conflict = next((c for c in conflicts if c["conflict_type"] == "EXTENT_MISMATCH"), None)
    assert extent_conflict is not None
    assert extent_conflict["status"] == "POSSIBLE_CONFLICT"

    mortgage_conflict = next((c for c in conflicts if c["conflict_type"] == "UNRELEASED_MORTGAGE"), None)
    assert mortgage_conflict is not None
    assert mortgage_conflict["status"] == "POSSIBLE_CONFLICT"

def test_workflow_005_title_search_report_generation(sample_deeds):
    timeline = timeline_builder.build_timeline(sample_deeds)
    conflicts = conflict_detector.detect_conflicts(sample_deeds)
    prop_details = {"survey_number": "42/1", "extent": "2 Acres 24 Guntas", "location": "Devanahalli"}

    report = report_builder.generate_report("mat_001", prop_details, timeline["timeline_nodes"], conflicts)
    assert "MATTER mat_001" in report["title"]
    assert "LEGAL DISCLAIMER" in report["disclaimer"]
    assert report["review_status"] == "APPROVED_FOR_EXPORT"
