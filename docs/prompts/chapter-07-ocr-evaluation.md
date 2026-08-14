# Chapter 7 Prompt — OCR Evaluation Harness

```markdown
Act as an OCR evaluation scientist.

Read Chapters 1–7 and inspect the OCR implementation and benchmark.

Do not modify code initially.

For every benchmark document:
1. compare ground truth to OCR
2. calculate CER
3. calculate WER where meaningful
4. calculate exact-match accuracy for property/court identifiers
5. calculate entity precision/recall
6. classify failure modes
7. identify language/script failures
8. identify table/layout failures

Return:
- aggregate metrics
- per-document metrics
- worst failure examples
- likely root causes
- recommended fixes
- whether the system should PASS, REVIEW_REQUIRED or FAIL

Do not hide errors by averaging them away.
```
