# Property Timeline Builder & Chain of Title Graph Engine

from typing import List, Dict, Any

class PropertyTimelineBuilder:
    """Builds a chronological transaction graph from verified deeds and flags missing links."""

    @staticmethod
    def build_timeline(doc_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Sort events chronologically by execution date
        sorted_events = sorted(doc_events, key=lambda e: e.get("execution_date", ""))
        
        timeline_nodes = []
        gaps = []

        for idx, event in enumerate(sorted_events):
            timeline_nodes.append({
                "event_id": f"evt_{idx + 1}",
                "execution_date": event.get("execution_date"),
                "event_type": event.get("event_type", "SALE_DEED"),
                "executant": event.get("executant"),
                "claimant": event.get("claimant"),
                "extent": event.get("extent"),
                "document_id": event.get("document_id"),
                "page_number": event.get("page_number", 1)
            })

            # Detect title chain gaps > 3 years between consecutive transactions
            if idx > 0:
                prev_year = int(sorted_events[idx - 1].get("execution_date", "1900")[:4])
                curr_year = int(event.get("execution_date", "1900")[:4])
                if (curr_year - prev_year) > 3:
                    gaps.append({
                        "from_year": prev_year,
                        "to_year": curr_year,
                        "warning": f"Title gap of {curr_year - prev_year} years between Deed {idx} and Deed {idx + 1}."
                    })

        return {
            "timeline_nodes": timeline_nodes,
            "title_gaps": gaps,
            "total_transactions": len(timeline_nodes)
        }

timeline_builder = PropertyTimelineBuilder()
