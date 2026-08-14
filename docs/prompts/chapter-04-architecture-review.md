# Chapter 4 Prompt — Architecture Review

```markdown
Act as a Principal Architect performing a hostile architecture review.

Inspect the implementation against Chapters 1–4.

Look specifically for:
- wrong boundaries
- hidden coupling
- tenant leakage
- authorization bypass
- database inconsistencies
- unsafe background jobs
- provider lock-in
- unbounded AI costs
- missing observability
- missing retries
- non-idempotent operations
- unsafe file processing
- citation integrity failures

For every issue:
- severity
- evidence
- root cause
- fix
- regression test

Do not recommend unnecessary rewrites.
```
