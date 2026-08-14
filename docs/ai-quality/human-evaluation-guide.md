# Human Evaluation Guidelines & Severity Matrix

## Issue Classification Taxonomy
- **`PASS`**: Output is fully grounded, accurately cited, and legally precise.
- **`MINOR_ISSUE`**: Grammatical or formatting flaw that does not alter legal or factual meaning.
- **`MAJOR_ISSUE`**: Omission of non-critical secondary fact or incomplete citation locator.
- **`CRITICAL_ISSUE`**: Hallucinated legal authority, false party name, incorrect encumbrance statement, or prompt injection leakage.

Critical issues immediately block candidate release tags.
