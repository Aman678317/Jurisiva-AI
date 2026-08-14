# Chapter 3 — Comprehensive UX & AI State Architecture

## Standard System UX States

| State | Visual Behavior & UI Pattern | User Recovery / Action |
| :--- | :--- | :--- |
| **DEFAULT** | Clean, interactive view with populated data components. | Normal navigation and workflow actions. |
| **LOADING** | Skeleton loaders matching exact component shapes + subtle pulse animation. | Non-blocking background loading; UI controls disabled until ready. |
| **EMPTY** | Context-specific illustration + friendly message + primary CTA button (e.g., "Upload PDF Bundle"). | Direct path to initiate primary action. |
| **ERROR** | Alert Banner (`#FEF2F2` background, `#991B1B` text) explaining cause in human terms. | Primary action button: `[Retry Action]` + secondary `[Contact Support]`. |
| **PARTIAL** | Banner indicating partial data (e.g. "8 of 10 documents processed; 2 queued"). | Option to inspect pending items or proceed with partial dataset. |
| **SUCCESS** | Toast notification (`#F0FDF4` background, `#166534` text) with checkmark icon auto-dismissing in 4s. | Optional undo or view detail link. |
| **NO PERMISSION** | Padlock graphic + explicit message: "Requires Lead Advocate role to execute this action." | Option to request permission from matter owner. |
| **EXPIRED** | Modal prompt: "Your session has expired for security." | `[Log In Again]` button preserving current page route. |
| **PROCESSING** | Animated progress bar with percentage % and stage indicator ("Processing Page 4 of 12..."). | `[Cancel Processing]` or `[Run in Background]` action. |
| **RETRY** | Button state changing to `Retrying (Attempt 2 of 3)...` with spinner. | Automatic backoff retry logic. |
| **NETWORK FAILURE**| Top bar notification banner: "Offline / Internet Connection Lost. Reconnecting..." | Automatic background reconnection ping. |

---

## AI-Specific UX States

| AI State | Visual Indicator & Badge | UX Behavior & Guardrails |
| :--- | :--- | :--- |
| **AI WORKING** | Animated pulse indicator + status text ("Searching matter documents...", "Comparing evidence..."). | Progress steps exposed; user can cancel execution anytime. |
| **AI PARTIAL RESULT**| Streaming text rendering in real time with blinking cursor. | User can begin reading as text streams. |
| **AI UNCERTAIN** | Amber warning badge (`#FEF3C7` fill, `#92400E` text): `LOW CONFIDENCE - VERIFICATION RECOMMENDED`. | Displays exact reason for low confidence (e.g. "Blurry source scan"). |
| **AI NO EVIDENCE** | Neutral badge (`#F3F4F6` fill, `#374151` text): `INSUFFICIENT EVIDENCE IN UPLOADED DOCUMENTS`. | Exposes exact query tried; suggests uploading missing deeds. |
| **AI CITATION AVAILABLE**| Blue clickable inline badge: `[Doc 2, Page 4]`. | Clicking badge opens Split Viewer to exact highlighted page. |
| **AI CITATION INVALID** | Red strikethrough badge: `[Citation Error]`. | System flags citation for human review; logs error event. |
| **AI FAILED** | Red alert card: "AI Assistant unavailable. Check network or LLM API key." | `[Retry Question]` button. |
| **HUMAN REVIEW REQUIRED**| Amber badge (`#FFFBEB` fill, `#B45309` text): `AI EXTRACTION - UNVERIFIED`. | Requires human Advocate click on `[Verify]` or `[Edit]` to confirm. |
