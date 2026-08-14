# Chapter 3 — Legal & Matter Research UX Architecture

## Research Workflow Architecture

```
RESEARCH DASHBOARD (RES-01 / AI-01)
  ↓
1. ENTER RESEARCH QUESTION
   └── User types natural language prompt or selects preset legal query
  ↓
2. SOURCE DISCOVERY & AUTHORIZATION
   └── System identifies authorized matter documents matching query scope
  ↓
3. HYBRID RETRIEVAL & RANKING
   └── Runs BM25 + pgvector similarity search across matter vector index
  ↓
4. ANSWER SYNTHESIS & CITATION INJECTION
   └── LLM generates structured answer with inline [Doc, Page] citations
  ↓
5. CONFLICT & UNCERTAINTY HANDLING
   └── Flags conflicting document statements or marks low-confidence answers
  ↓
6. RESEARCH HISTORY & EXPORT
   └── Saves query session to matter research log; allows export to report notes
```

---

## Source Status Classification Standards
To ensure complete transparency, every source passage evaluated during research carries an explicit status:

- **SOURCE FOUND**: Document passage retrieved matching query vector distance threshold.
- **SOURCE VERIFIED**: Passage text confirmed against raw OCR layer with active citation link.
- **SOURCE UNAVAILABLE**: Query requested information absent in uploaded document bundle.
- **SOURCE CONFLICTED**: Multiple document passages state conflicting facts regarding the query.

---

## Copilot & Research UI Controls (`AI-01`)

### Input Area
- Textarea with auto-expansion up to 150px height.
- Scope Selector Dropdown: `[All Matter Docs]` | `[Deeds Only]` | `[EC Only]` | `[Pahani/RTC Only]`.
- Action Buttons: `[Send Question (Enter)]` | `[Preset Prompts]`.

### Streaming Output Area
- Real-time status progress pill ("Searching 15 documents...", "Comparing evidence...").
- Formatted Markdown response text.
- Inline blue citation buttons `[Doc 2, Page 4]`.
- Response Actions Footer: `[Inspect Source]` | `[Copy Markdown]` | `[Regenerate Response]` | `[Report Error]`.
