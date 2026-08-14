# Architectural & Product Decision Log (ADR)

## ADR-001: India-First Focus & Property Due-Diligence Priority
- **Status**: Approved
- **Decision**: Prioritize Property Due-Diligence and Title Search as the initial primary workflow for MVP validation.

## ADR-002: Human-in-the-Loop Verification Framework
- **Status**: Approved
- **Decision**: Design explicit multi-state data tagging for all system outputs (`SOURCE FACT`, `AI EXTRACTION`, `AI INFERENCE`, `HUMAN VERIFIED`, `UNKNOWN`).

## ADR-003: Replaceable LLM Orchestration Layer
- **Status**: Approved
- **Decision**: Abstract all LLM calls through a standardized unified adapter layer.

## ADR-004: Free/Open-Source Infrastructure First
- **Status**: Approved
- **Decision**: Standardize on PostgreSQL + pgvector, FastEngine/FastAPI, and local open-source OCR engines.
