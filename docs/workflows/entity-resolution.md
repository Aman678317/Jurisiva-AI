# Cautious Entity Resolution Engine

## Matching Criteria & Decision Matrix
| Name Signal | Address Signal | Father/Spouse Signal | Result | Action |
| :--- | :--- | :--- | :---: | :--- |
| Exact match | Exact match | Exact match | `MATCH` | Auto-link in timeline |
| Exact match | Partial / Different | Matching | `POSSIBLE_MATCH` | Flag for advocate review |
| Phonetic similarity ("Rajesh" / "Rajesha") | Matching | Matching | `POSSIBLE_MATCH` | Flag for advocate review |
| Name match only | Different | Unknown | `REVIEW_REQUIRED` | Do NOT merge automatically |

Never merge two entities automatically unless exact name, parentage, and address signals match.
