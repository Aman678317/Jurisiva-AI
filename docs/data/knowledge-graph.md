# Governed Knowledge Graph Architecture

## Governed Graph Relationships & Provenance
Every edge in the Property Evidence Graph retains full provenance metadata:

```json
{
  "edge_id": "edge_001",
  "source_entity": "person_venkatappa",
  "relationship": "TRANSFERRED_TITLE_TO",
  "target_entity": "person_krishnappa",
  "provenance": {
    "source_id": "doc_1985",
    "page_number": 1,
    "extraction_method": "INDIC_OCR_PIPELINE",
    "confidence": 0.96,
    "review_status": "SUPPORTED"
  }
}
```

Cross-tenant graph traversal is strictly prevented at database query execution.
