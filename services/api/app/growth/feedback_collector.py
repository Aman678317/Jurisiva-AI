# Customer Feedback & AI Regression Fixture Collector

import time
from typing import Dict, List, Any

class CustomerFeedbackCollector:
    """Collects advocate feedback on AI citations and generates regression fixtures for failing queries."""

    def __init__(self):
        self._feedback_records: List[Dict[str, Any]] = []

    def record_feedback(self, org_id: str, user_id: str, run_id: str, rating: str, comment: str, is_citation_error: bool) -> Dict[str, Any]:
        record = {
            "feedback_id": f"FBK-{int(time.time())}",
            "org_id": org_id,
            "user_id": user_id,
            "run_id": run_id,
            "rating": rating,
            "comment": comment,
            "is_citation_error": is_citation_error,
            "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        self._feedback_records.append(record)

        # Automatically flag for regression fixture generation if citation error
        if is_citation_error:
            record["regression_fixture_status"] = "QUEUED_FOR_REGRESSION_TEST"

        return record

feedback_collector = CustomerFeedbackCollector()
