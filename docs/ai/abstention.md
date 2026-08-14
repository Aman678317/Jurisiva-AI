# Abstention & Refusal Protocol

## Negative Query Refusal Policy
When retrieved evidence fails to meet minimum relevance or sufficiency thresholds, the system must gracefully refuse to answer rather than fabricating plausible legal claims.

## Refusal Response Standard Format
```json
{
  "answer": "Insufficient evidence in the uploaded documents to answer this question reliably.",
  "evidence_status": "INSUFFICIENT_EVIDENCE",
  "searched_scope": {
    "matter_id": "mat_001",
    "retrieved_chunk_count": 0
  },
  "citations": [],
  "warnings": ["No relevant document chunks met the evidence sufficiency threshold."]
}
```
