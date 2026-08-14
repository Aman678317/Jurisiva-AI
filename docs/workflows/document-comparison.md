# Document Comparison & Side-by-Side Diff Specification

## Comparison Engine Specs
- **Inputs**: Document Version A ID & Document Version B ID.
- **Normalization**: Line break and whitespace cleanup applied prior to diffing.
- **Diff Classification**:
  - `ADDED`: Text present in B but absent in A.
  - `REMOVED`: Text present in A but absent in B.
  - `MODIFIED`: Text updated between A and B (e.g. consideration amount changed from ₹50,00,000 to ₹60,00,000).
- **UI Contract**: Split-screen canvas highlighting additions in green (`#DCFCE7`) and deletions in red (`#FEE2E2`).
