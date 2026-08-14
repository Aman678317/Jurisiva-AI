# Chapter 8 Prompt — Hybrid Retrieval Engine

```markdown
Implement hybrid retrieval.

Pipeline:
authorized corpus
→ lexical retrieval
→ semantic retrieval
→ merge
→ optional rerank
→ evidence results

Evaluate:
- exact queries
- semantic queries
- metadata queries
- multilingual queries
- negative queries
- conflicting evidence

Return evidence with provenance.
Do not hide uncertainty behind a relevance score.
```
