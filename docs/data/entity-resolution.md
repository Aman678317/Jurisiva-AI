# Entity Resolution Rules & Candidate Matching

## Entity Resolution Scoring Matrix

| Matching Signals | Candidate Match Status | Action Required |
| :--- | :---: | :--- |
| **Exact Identifier Match** (Survey No + Village) | `MATCH` | Entity linked automatically |
| **Name + Address Similarity** (> 85% match) | `POSSIBLE_MATCH` | Queued for advocate review |
| **Discrepant Extent / Discrepant Date** | `REVIEW_REQUIRED` | Flagged as potential conflict |
| **Different Village / Different District** | `NO_MATCH` | Kept as distinct entities |

Zero false merges permitted for property parcel identity.
