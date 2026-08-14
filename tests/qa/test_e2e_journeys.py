# End-to-End Property Intelligence User Journey Test Suite (Journey 2)

import pytest
from app.workflows.property_timeline import timeline_builder
from app.workflows.entity_resolution import entity_resolver
from app.workflows.conflict_detector import conflict_detector

def test_e2e_002_property_title_diligence_workflow():
    deeds = [
        {"document_id": "doc_1985", "execution_date": "1985-08-14", "event_type": "SALE_DEED", "executant": "Venkatappa", "claimant": "Krishnappa", "extent": "2 Acres 24 Guntas", "page_number": 1},
        {"document_id": "doc_2018", "execution_date": "2018-11-12", "event_type": "SALE_DEED", "executant": "Krishnappa", "claimant": "Anand Kumar", "extent": "2 Acres 10 Guntas", "page_number": 2}
    ]

    # 1. Entity Resolution Check
    ent_res = entity_resolver.resolve_entity({"name": "Krishnappa", "address": "Devanahalli"}, {"name": "Krishnappa", "address": "Devanahalli"})
    assert ent_res["status"] == "MATCH"

    # 2. Title Timeline Assembly
    timeline = timeline_builder.build_timeline(deeds)
    assert len(timeline["timeline_nodes"]) == 2

    # 3. Extent Mismatch Conflict Detection
    conflicts = conflict_detector.detect_conflicts(deeds)
    assert len(conflicts) > 0
    assert conflicts[0]["status"] == "POSSIBLE_CONFLICT"
