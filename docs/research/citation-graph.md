# Citation Graph Engine & Precedent Relationship Model

## Precedent Relationship Types
- **`CITES`**: Direct citation reference to prior judgment or statutory section.
- **`FOLLOWS`**: Adopts principles set out in earlier precedent.
- **`DISTINGUISHES`**: Differentiates factual matrix from prior precedent.
- **`OVERRULES`**: Higher bench formally overrules earlier holding.

## Provenance Enforcement
No citation edge (e.g. `Case A OVERRULES Case B`) is stored in the graph without exact source document page locators and confidence metadata.
