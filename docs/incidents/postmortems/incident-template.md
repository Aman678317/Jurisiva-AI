# Blameless Incident Postmortem Template

```markdown
# Incident Postmortem: [INCIDENT TITLE]

## Executive Summary
- **Incident ID**: INC-YYYYMMDD-XX
- **Severity**: SEV-1 | SEV-2 | SEV-3
- **Start Time**: YYYY-MM-DD THH:MM:SSZ
- **Resolution Time**: YYYY-MM-DD THH:MM:SSZ
- **Total Duration**: XX minutes
- **Impacted Systems**: [e.g., Ingestion Worker, RAG Search API]

## Root Cause Analysis
Explain the underlying technical root cause. Focus on system design gaps rather than human error.

## Timeline of Events
- **HH:MM**: Detection via automated alert.
- **HH:MM**: Incident Commander assigned; containment initiated.
- **HH:MM**: Fix deployed; health verified.

## Corrective Actions & Preventative Items
1. [Action Item 1]: Owner: [Name], Due: [Date], Ticket: [ID]
2. [Regression Test]: Added test in `tests/regression/`.
```
