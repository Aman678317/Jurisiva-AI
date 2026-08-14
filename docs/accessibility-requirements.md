# Chapter 3 — Accessibility & Indic Script Requirements (WCAG 2.1 AA)

## Accessibility Standards Compliance

### 1. Keyboard Navigation & Focus Management
- **Focus Rings**: All interactive elements (buttons, inputs, citations, links) display a high-contrast focus ring (`2px solid #2563EB`, offset 2px).
- **Keyboard Shortcuts**:
  - `Cmd+K` / `Ctrl+K`: Open Global Search.
  - `PageUp` / `PageDown`: Turn document pages in Viewer.
  - `Esc`: Close modals, drawers, citation popovers.
  - `Tab` / `Shift+Tab`: Logical tab order across all workspace panels.

### 2. Screen Reader Semantics & ARIA Landmarks
- Proper HTML5 semantic structure: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`.
- ARIA Roles: `role="dialog"` for modals, `role="alert"` for red-flag conflict banners, `aria-live="polite"` for AI streaming text.
- Form Inputs: Explicit `<label>` elements associated with `id` for screen readers.

### 3. Color Contrast & Visual Standards
- Minimum 4.5:1 contrast ratio for normal text; 3:0:1 for large headings and icons against background.
- Information NEVER communicated by color alone (e.g. Red-flag alerts include text badge `CRITICAL DEFECT` + warning icon).

### 4. Indic Script Rendering & Encoding
- **Encoding**: Strict UTF-8 text encoding across database, backend APIs, and UI components.
- **Font Stack**: Includes `Noto Sans Indic` ensuring correct rendering of complex Indic ligatures and conjunct characters (Hindi, Kannada, Marathi, Tamil, Telugu).
- **Numeral Preservation**: Original document numbers, survey numbers, and dates preserved in exact digits without character corruption.
