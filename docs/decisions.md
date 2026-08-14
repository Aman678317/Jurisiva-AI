# Architectural & Product Decision Log (ADR)

## ADR-001: India-First Focus & Property Due-Diligence Priority
- **Status**: Approved
- **Context**: Legal technology in India suffers from high document fragmentation, heavy reliance on scanned/handwritten Indic regional documents, and complex property title verification workflows.
- **Decision**: Prioritize Property Due-Diligence and Title Search as the initial primary workflow for MVP validation.
- **Consequences**: Architecture must support Indic multilingual OCR (Tesseract / PaddleOCR / EasyOCR), split-screen verification UI, and property-specific domain extraction schema (Survey numbers, Khasra, EC, Pahani).

## ADR-002: Human-in-the-Loop Verification Framework
- **Status**: Approved
- **Context**: Consequential legal and property transactions require absolute accountability under Indian law.
- **Decision**: Design explicit multi-state data tagging for all system outputs: `SOURCE FACT`, `AI EXTRACTION`, `AI INFERENCE`, `HUMAN VERIFIED`, and `UNKNOWN`.
- **Consequences**: UI components must display badges indicating verification state, and final reports must highlight unverified AI inferences.

## ADR-003: Replaceable LLM Orchestration Layer
- **Status**: Approved
- **Context**: LLM pricing, capability, and local deployment options (e.g. Ollama, vLLM, OpenAI, Anthropic, Gemini) evolve rapidly.
- **Decision**: Abstract all LLM calls through a standardized unified adapter layer (LiteLLM / custom interface).
- **Consequences**: Switching models requires changing environment variables without modifying RAG or prompt pipeline code.

## ADR-004: Free/Open-Source Infrastructure First
- **Status**: Approved
- **Context**: Minimize early capital expenditure and maintain low cost per matter processed (< ₹150).
- **Decision**: Standardize on PostgreSQL + pgvector for relational and vector storage, Tesseract/PaddleOCR for OCR, and FastEngine/FastAPI for backend logic.
- **Consequences**: Keeps infrastructure lightweight, single-node deployable, and zero vendor lock-in.
