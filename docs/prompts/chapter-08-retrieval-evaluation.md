# Chapter 8 Prompt — Retrieval Evaluation Harness

```markdown
Build a retrieval evaluation harness.

For every query:
- authorized corpus
- expected evidence
- retrieved evidence
- rank
- latency

Measure:
- Recall@K
- Precision@K
- MRR
- nDCG where useful
- source coverage

Break down results by:
- workflow
- language
- query type

Compare every change against baseline.
Block release on critical retrieval regression.
```
