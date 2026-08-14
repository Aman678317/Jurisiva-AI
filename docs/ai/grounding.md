# Grounding & Evidence Evaluation

## Grounding Evaluation States
1. **GROUNDED**: Every factual assertion maps to a verified source document chunk with exact page location.
2. **PARTIALLY_GROUNDED**: Core statements are supported by evidence, but additional context or inference is drawn.
3. **UNSUPPORTED**: Information cannot be mapped to authorized retrieved document chunks.
4. **CONFLICTED**: Multiple authorized documents contain contradictory facts (e.g. Sale Deed 1985 lists Owner A, while Tax Receipt 2010 lists Owner B).

## Conflict Handling Rule
When contradictory evidence exists across authorized documents, the system MUST NOT silently select one document. It MUST surface both conflicting sources with their respective document dates and page numbers for advocate review.
