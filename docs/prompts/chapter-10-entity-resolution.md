# Chapter 10 Prompt — Cautious Entity Resolution

```markdown
Implement cautious entity resolution.

Match entities using approved evidence.

Possible signals:
- name
- address
- identifier
- context
- date
- document relationships

Never silently merge uncertain entities.

Return:
- MATCH
- POSSIBLE_MATCH
- NO_MATCH
- REVIEW_REQUIRED

Include evidence for the decision.
```
