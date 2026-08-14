# Document Review & Property Due Diligence Workflows

## 1. Document Review Specification
- **Flow**: Upload -> Validate -> OCR -> Chunk -> Extract Key Facts -> Review.
- **Extracted Fields**: Parties (Executant/Claimant), Property Identifiers (Survey #, Hissa #, Extent), Consideration Amount, Registration References, Encumbrance Flags.
- **Evidence Requirement**: Every key fact contains clickable page coordinates `[Doc ID, Page Num]`.

## 2. Document Comparison Specification
- **Flow**: Select Document A & Document B -> Align Sections -> Compute Diff -> Classify Changes -> Display Split Viewer.
- **Diff Types**: `ADDED`, `REMOVED`, `MODIFIED`, `UNCHANGED`.
- **Safety Boundary**: Changes are presented strictly as text/clause differences without legal enforceability judgments.
