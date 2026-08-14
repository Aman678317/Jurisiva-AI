# Evidence-Aware Entity Resolution & Match Confidence Model

## Entity Match Confidence States

| Match Confidence | Matching Signal Criteria | Automated Merge Policy |
| :--- | :--- | :---: |
| **`EXACT`** | Unique Identifier Match (PAN, Survey No, Case ID) | Permitted |
| **`LIKELY`** | Name + Address + Co-owner context overlap | Review Required |
| **`POSSIBLE`** | Name similarity > 85% without address match | Flagged Candidate |
| **`CONFLICTED`** | Contradictory ownership records on same property | Escalated to Review Queue |
| **`UNKNOWN`** | Insufficient metadata attributes | Unlinked Entity |

Uncertain entities are NEVER merged automatically without evidence review.
