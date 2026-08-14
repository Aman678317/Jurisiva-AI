# Side-by-Side Document Comparator Engine

from typing import Dict, List, Any

class DocumentComparator:
    """Computes line-by-line diffs between Document A and Document B."""

    @staticmethod
    def compare_documents(doc_a_text: str, doc_b_text: str) -> Dict[str, Any]:
        lines_a = [l.strip() for l in doc_a_text.split("\n") if l.strip()]
        lines_b = [l.strip() for l in doc_b_text.split("\n") if l.strip()]
        
        diffs = []
        set_a = set(lines_a)
        set_b = set(lines_b)

        # Removed lines
        for line in lines_a:
            if line not in set_b:
                diffs.append({"type": "REMOVED", "text": line, "source": "Document A"})

        # Added lines
        for line in lines_b:
            if line not in set_a:
                diffs.append({"type": "ADDED", "text": line, "source": "Document B"})

        # Unchanged count
        unchanged_count = len(set_a.intersection(set_b))

        return {
            "diffs": diffs,
            "added_count": sum(1 for d in diffs if d["type"] == "ADDED"),
            "removed_count": sum(1 for d in diffs if d["type"] == "REMOVED"),
            "unchanged_count": unchanged_count
        }

document_comparator = DocumentComparator()
