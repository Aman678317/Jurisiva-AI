# Conflict Detection Specification

## Conflict Detection Engine Rules
1. **Extent Discrepancy**: Deed A specifies extent as `2 Acres 24 Guntas`, but subsequent Deed B specifies `2 Acres 10 Guntas`. Output: `POSSIBLE_CONFLICT: Extent mismatch between Deed A (p.3) and Deed B (p.2)`.
2. **Unreleased Mortgage Conflict**: Mortgage Deed present in timeline without matching Release/Reconveyance Deed within 30 years. Output: `POSSIBLE_CONFLICT: Active unreleased mortgage encumbrance`.
3. **Owner Name Discrepancy**: RTC lists Owner X while latest registered Sale Deed lists Owner Y. Output: `POSSIBLE_CONFLICT: Revenue record owner mismatch`.

## Safety Output Standard
Output status is strictly `POSSIBLE_CONFLICT` with clickable source page citations. Labels such as "Fraud" or "Invalid Title" are strictly forbidden.
