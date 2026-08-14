# Chapter 3 — Responsive UX Strategy

## Responsive Breakpoint Tokens
- Desktop Wide (`desktop-wide`): `>= 1440px`
- Desktop Standard (`desktop`): `1280px – 1439px`
- Tablet (`tablet`): `768px – 1279px`
- Mobile (`mobile`): `< 768px`

---

## Screen Adaptation Matrix

| Screen | Desktop Layout Strategy | Tablet Adaptation | Mobile Adaptation |
| :--- | :--- | :--- | :--- |
| **DOC-03 Split Viewer** | Dual-pane 50/50 side-by-side canvas with live highlight. | 60/40 side-by-side view with collapsible right panel. | Single pane with toggle button (`[Show PDF]` / `[Show Text]`). Banner recommends desktop. |
| **PROP-01 Dashboard** | 3-column layout (Timeline, Schedule, Verification panel). | 2-column layout (Timeline + Schedule; Verification panel in drawer). | Single column vertical stack with bottom sheet review drawer. |
| **AI-01 Copilot** | Integrated side panel or 2-column workspace. | Collapsible slide-over drawer. | Full-screen conversation view with bottom fixed input. |
| **MAT-01 Matter Table** | 7-column data table (Title, Client, Status, Docs, Created, Actions). | 5-column data table (Hides Created Date & Hash). | Card list view displaying Title, Status badge, and Doc Count. |
