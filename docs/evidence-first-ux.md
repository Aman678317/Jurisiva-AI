# Chapter 3 — Evidence-First UX Architecture

## Core Evidence Principles
1. **Zero Decorative Citations**: Every citation badge `[Doc X, Page Y]` MUST resolve to a real document page and bounding-box snippet.
2. **Instant Verification (< 300ms)**: Clicking a citation must immediately open the source PDF view without full page reloads.
3. **Dual Provenance Display**: Always display both the scanned original PDF snippet and the extracted raw text layer simultaneously.

---

## Evidence Component Interaction Design

```
AI Claim or Summary Text
  └── Inline Citation Badge: [Doc 2 (Sale Deed), Page 4, Para 3]
        ↓ Click
  Split Viewer Canvas Opens (DOC-03)
  ├── Left Pane: PDF Page 4 loaded; yellow bounding box (#FEF08A) rendered over text.
  └── Right Pane: Extracted OCR Text + Metadata Card (SHA-256 Hash, Upload Date, File Name).
```

---

## Detailed Evidence UI Elements

### 1. Citation Interaction & Popover
- Hovering citation `[Doc 2, Page 4]` renders a mini popover showing:
  - Document Name: `Sale Deed 1985.pdf`
  - Page Number: `Page 4 of 12`
  - Text Snippet Preview: `"...all that piece and parcel of land measuring 2,400 sq.ft..."`
  - Action Link: `[Open in Split Viewer]`

### 2. Visual Page Locator & Bounding Box Highlight
- When opened in `DOC-03`, the canvas automatically scrolls to center the snippet.
- Bounding Box Highlight styling:
  - Fill: `rgba(254, 240, 138, 0.45)` (Yellow 200 at 45% opacity)
  - Border: `2px solid #CA8A04` (Yellow 600)
  - Pulse animation (2 iterations) to draw user's eyes to the exact location.

### 3. Source Metadata & Freshness
Every evidence drawer displays immutable provenance metadata:
- Document Title & Category badge.
- File SHA-256 Hash.
- Upload Date & Uploaded By User.
- OCR Confidence Score & Processing Timestamp.

### 4. Conflicting Evidence UI Pattern
When two documents state conflicting facts:
- Displays a Side-by-Side Comparison Card:
  - **Source A**: `1985 Sale Deed (Doc 1, Page 3)` -> Extent: `2,400 sq.ft`.
  - **Source B**: `2012 Partition Deed (Doc 4, Page 2)` -> Extent: `2,100 sq.ft`.
- Both sources include direct `[Inspect]` buttons jumping to their respective document views.

### 5. Missing Evidence UI Pattern
When required evidence is absent in the uploaded bundle (e.g. Missing 1995 Link Deed):
- Renders an Amber Gap Card: `MISSING LINK DEED (1995 to 2004)`.
- Action CTA: `[Upload Missing Link Deed]` or `[Mark as Unobtainable with Advocate Note]`.
