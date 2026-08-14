# Chapter 3 — Visual Design System & Token Specifications

## Design Philosophy & Tone
The UI must communicate **trust, evidence, clarity, calm, and security**. It should feel like high-grade professional legal infrastructure (dense, legible, fast, calm), avoiding decorative fluff, trendy gradients, or distraction.

---

## 1. Color Tokens (Tailored Palette)

```css
:root {
  /* Surfaces & Backgrounds */
  --surface-default: #FAFAFA;
  --surface-raised: #FFFFFF;
  --surface-overlay: #F3F4F6;
  --surface-muted: #E5E7EB;

  /* Brand / Primary (Deep Navy - Trust & Legal Authority) */
  --primary-default: #0F172A; /* Slate 900 */
  --primary-hover: #1E293B;   /* Slate 800 */
  --primary-active: #334155;  /* Slate 700 */
  --primary-fg: #FFFFFF;

  /* Neutral Text Hierarchy */
  --text-primary: #0F172A;   /* High contrast body */
  --text-secondary: #475569; /* Subtitles & labels */
  --text-muted: #64748B;     /* Captions & hints */
  --text-disabled: #94A3B8;

  /* Evidence & Verification Badges */
  --badge-source-fact-bg: #EFF6FF;
  --badge-source-fact-fg: #1E40AF;
  --badge-ai-extraction-bg: #FEF3C7;
  --badge-ai-extraction-fg: #92400E;
  --badge-human-verified-bg: #F0FDF4;
  --badge-human-verified-fg: #166534;
  --badge-rejected-bg: #FEF2F2;
  --badge-rejected-fg: #991B1B;

  /* Citation Highlights */
  --highlight-citation-fill: rgba(254, 240, 138, 0.5); /* Yellow 200 at 50% */
  --highlight-citation-border: #CA8A04;                 /* Yellow 600 */

  /* Status Colors */
  --status-success: #16A34A;
  --status-warning: #D97706;
  --status-error: #DC2626;
  --status-info: #2563EB;

  /* Borders & Focus Rings */
  --border-default: #E2E8F0;
  --border-strong: #CBD5E1;
  --focus-ring: 2px solid #2563EB;
}
```

---

## 2. Typography Stack & Indic Font Coverage

```css
:root {
  /* Font Family Stack: Inter for Latin/Numerals + Noto Sans for Indic Scripts */
  --font-sans: 'Inter', 'Noto Sans Indic', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* Scale */
  --text-xs: 0.75rem / 1.125rem;   /* 12px / 18px */
  --text-sm: 0.875rem / 1.25rem;   /* 14px / 20px */
  --text-base: 1rem / 1.5rem;      /* 16px / 24px */
  --text-lg: 1.125rem / 1.75rem;   /* 18px / 28px */
  --text-xl: 1.25rem / 1.75rem;    /* 20px / 28px */
  --text-2xl: 1.5rem / 2.0rem;     /* 24px / 32px */
}
```

---

## 3. Spacing & Grid Tokens
- Base unit: 4px grid (`--space-1: 4px`, `--space-2: 8px`, `--space-3: 12px`, `--space-4: 16px`, `--space-6: 24px`, `--space-8: 32px`).
- Layout widths: `--max-width-workspace: 1600px`.

---

## 4. Primitive UI Components Design Specifications

### Buttons
- **Primary**: Deep navy background (`--primary-default`), white text, 6px border radius, 40px height. High contrast.
- **Secondary**: White background, default border (`--border-default`), dark text.
- **Ghost / Icon**: Transparent background, hover tint.

### Data Tables (`DataTable`)
- Dense, highly readable rows (44px row height).
- Sticky table headers with subtle bottom border (`--border-default`).
- Zebra striping option for multi-column data views.

### Verification & Status Badges
- Pill-shaped (`border-radius: 9999px`), 12px font size, uppercase letter-spacing (0.05em).
- `SOURCE FACT` (Blue), `AI EXTRACTION` (Amber), `HUMAN VERIFIED` (Green), `REJECTED` (Red).

### Citation Components
- `CitationBadge`: Small inline tag `[Doc 2, Page 4]`, blue tint, cursor pointer. Hover state displays preview popover.
- `CitationHighlight`: Yellow bounding box overlay rendered on PDF canvas.
