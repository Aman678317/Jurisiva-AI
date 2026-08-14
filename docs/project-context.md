# Project Context & Repository Blueprint

## System Summary
- **Name**: India-First Legal & Property Intelligence Platform
- **Architecture**: Decoupled Client-Server / RAG-driven AI Workflows / Micro-modular Pipeline
- **Core Domain**: Indian Legal Document Analysis, Property Title Search & Due Diligence

## Core Principles
1. **Human-in-the-Loop**: Consequential legal/property assessments require human review and confirmation.
2. **Evidence-Grounded AI**: Every AI assertion is backed by verifiable, traceable citations with page and bounding box pinpointing.
3. **India-First Engineering**: Native support for Indic multilingual OCR (Hindi, Kannada, Tamil, Marathi, Telugu, Bengali), Indian land record terminology (Khasra/Khatauni, RTC/Pahani, EC, Patta, Sale Deed, Partition Deed, GPA), and Indian court citation standards.
4. **Data Isolation & Security**: Matter-based workspace partitioning, field-level encryption, role-based access control, and complete audit logging.
5. **No Proprietary Lock-In**: Standard open formats, open-source model compatibility, zero vendor lock-in.

## Implementation Guidelines
- Follow the 32-Chapter Production Build Bible sequentially.
- Pass strict verification gates before proceeding between chapters.
- Maintain comprehensive documentation across `docs/` and root memory files.
