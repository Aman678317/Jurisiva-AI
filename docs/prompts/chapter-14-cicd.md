# Chapter 14 Prompt — CI/CD Pipeline

```markdown
Act as a Principal DevOps Engineer.

Implement the production CI/CD pipeline.

Required flow:
PR → lint/typecheck → tests → security scans → build → immutable artifact → staging → smoke/E2E → release approval → production → health validation

Never deploy a failing build.
Never rebuild different code between staging and production.
Implement rollback and deployment evidence.
```
