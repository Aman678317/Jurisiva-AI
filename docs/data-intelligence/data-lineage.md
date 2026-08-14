# End-to-End Data Lineage & Provenance Map

## Data Provenance Pipeline

```text
SOURCE DEED (PDF)
  ↓ (OCR Engine:IndicOCR)
CANONICAL DOCUMENT METADATA (PostgreSQL)
  ↓ (Entity Extractor:GovernedLLM)
EXTRACTED ENTITIES (Party / Property)
  ↓ (Entity Resolver:EntityResolver)
RESOLVED ENTITY (Confidence: EXACT / LIKELY)
  ↓ (Graph Builder:ProvenanceKnowledgeGraph)
TEMPORAL KNOWLEDGE GRAPH EDGE (OWNS / CITES)
```

Every derived object stores `source_document_id`, `page_number`, `bounding_box`, and `extractor_version`.
