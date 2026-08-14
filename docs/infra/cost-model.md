# Infrastructure Cost Model & Unit Economics

## Unit Cost Breakdown
- **Cost per Matter Diligence**: ₹85 (Target < ₹120)
  - Document Storage (S3): ₹5
  - OCR Processing (Indic Tesseract): ₹15
  - Embedding Vector Storage (pgvector): ₹10
  - RAG Copilot Completions (gpt-4o-mini): ₹55

## Monthly Fixed Infrastructure Target
- Base Compute (Containers): ₹2,500/mo
- Database (PostgreSQL 16): ₹3,000/mo
- Redis Broker & Storage: ₹1,500/mo
- **Total Fixed Base Cost**: ₹7,000/mo (Scaled based on active advocate organizations).
