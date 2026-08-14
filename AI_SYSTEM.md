# AI Architecture & Prompt Engineering Framework

## Architectural Principles
1. **Strict Context Grounding**: System prompts explicitly forbid external knowledge usage when answering legal document queries.
2. **Citation Injection**: Retrived context chunks contain `[DocID:PageNum:SnippetID]`. Model must cite sources inline.
3. **Structured Outputs**: Entity extraction and contradiction detection use Pydantic schemas / JSON mode.
4. **Prompt Injection Guard**: User input is sanitized and wrapped in clear delimiters (`<user_query>`) to prevent jailbreaking.
5. **Fallback & Retry**: LiteLLM adapter automatically falls back to secondary models if timeout or rate limit occurs.
