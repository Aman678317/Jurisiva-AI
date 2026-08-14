# Chapter 3 — Reusable Component Inventory

## Component Library Overview (20 Core Components)

### 1. AppShell
- **PURPOSE**: Master layout container rendering top bar, sidebar navigation, and main content area.
- **PROPS**: `children: ReactNode`, `activeRoute: string`, `currentUser: User`.
- **STATES**: Sidebar collapsed/expanded, mobile drawer open/closed.
- **PERMISSIONS**: All authenticated users.
- **ACCESSIBILITY**: Landmark regions (`<header>`, `<nav>`, `<main>`), skip-to-content link.
- **RESPONSIVE**: Left sidebar collapses to icon drawer on tablet; turns into overlay drawer on mobile.

---

### 2. Sidebar
- **PURPOSE**: Main navigation drawer listing global app sections (Matters, Search, Settings).
- **PROPS**: `activePath: string`, `isCollapsed: boolean`, `onToggle: () => void`.
- **STATES**: Expanded, Collapsed.
- **PERMISSIONS**: All authenticated users.
- **ACCESSIBILITY**: `aria-expanded` state, keyboard arrow key navigation.
- **RESPONSIVE**: Collapses on screens < 1024px.

---

### 3. TopBar
- **PURPOSE**: Persistent top bar with Matter Switcher, Global Search input, Notifications, User Profile.
- **PROPS**: `currentMatter?: Matter`, `onSearchClick: () => void`.
- **STATES**: Default, Search Focused.
- **PERMISSIONS**: All authenticated users.
- **ACCESSIBILITY**: Focus trap on search popup, `role="toolbar"`.
- **RESPONSIVE**: Condenses search input to icon button on mobile.

---

### 4. MatterSwitcher
- **PURPOSE**: Fast dropdown selector for switching between active legal matters.
- **PROPS**: `matters: Matter[]`, `currentMatterId: string`, `onSelectMatter: (id: string) => void`.
- **STATES**: Closed, Open, Searching.
- **PERMISSIONS**: All authenticated users.
- **ACCESSIBILITY**: `role="combobox"`, `aria-autocomplete="list"`, Esc key closes dropdown.
- **RESPONSIVE**: Full width on mobile dropdown.

---

### 5. DocumentUploader
- **PURPOSE**: Drag-and-drop file upload zone for PDF bundles.
- **PROPS**: `matterId: string`, `onUploadComplete: (files: File[]) => void`, `maxSizeMB: number`.
- **STATES**: Idle, DragOver, Uploading, Processing, Error.
- **PERMISSIONS**: `LEAD_ADVOCATE`, `ASSOCIATE`.
- **ACCESSIBILITY**: File input labelled with screen reader instructions; keyboard focusable.
- **RESPONSIVE**: Stacked file list on smaller screens.

---

### 6. DocumentViewer
- **PURPOSE**: Split-screen PDF viewer with bounding-box canvas highlight overlay.
- **PROPS**: `documentUrl: string`, `currentPage: number`, `highlights: BoundingBox[]`, `onPageChange: (p: number) => void`.
- **STATES**: Loading, Loaded, Highlighting, Error.
- **PERMISSIONS**: All matter users.
- **ACCESSIBILITY**: Keyboard page turning (`PageUp` / `PageDown`), zoom controls with explicit labels.
- **RESPONSIVE**: Desktop split-pane; full-bleed single view on tablet/mobile with toggle.

---

### 7. EvidenceCard
- **PURPOSE**: Displays extracted document snippet with source metadata and citation badge.
- **PROPS**: `snippetText: string`, `docName: string`, `pageNum: number`, `citationId: string`.
- **STATES**: Default, Hover, Highlighted.
- **PERMISSIONS**: All matter users.
- **ACCESSIBILITY**: Citation badge focusable via Tab; screen reader reads snippet context.
- **RESPONSIVE**: Fluid width container.

---

### 8. Citation & CitationPopover
- **PURPOSE**: Interactive inline citation button `[Doc X, Page Y]` that displays source preview on hover/click.
- **PROPS**: `docId: string`, `docName: string`, `page: number`, `excerpt: string`.
- **STATES**: Default, Hover Popover Open, Active Selected.
- **PERMISSIONS**: All matter users.
- **ACCESSIBILITY**: `aria-haspopup="dialog"`, Esc key closes popover.
- **RESPONSIVE**: Popover repositioned within screen boundaries.

---

### 9. AIMessage & AIProgress
- **PURPOSE**: RAG assistant response container displaying markdown, streaming status, and inline citations.
- **PROPS**: `message: AIMessageObj`, `isStreaming: boolean`, `onInspectSource: (citationId: string) => void`.
- **STATES**: Streaming, Complete, Error, Low Confidence Warning.
- **PERMISSIONS**: All matter users.
- **ACCESSIBILITY**: `aria-live="polite"` during streaming.
- **RESPONSIVE**: Full container fluid width.

---

### 10. PropertyTimeline
- **PURPOSE**: Chronological vertical graph rendering property conveyances over 30 years.
- **PROPS**: `events: TimelineEvent[]`, `onSelectEvent: (id: string) => void`.
- **STATES**: Loading, Rendered, Gap Warning State.
- **PERMISSIONS**: All matter users.
- **ACCESSIBILITY**: List semantics (`<ul>`, `<li>`), keyboard focusable event cards.
- **RESPONSIVE**: Vertical single-column stack on mobile.

---

### 11. ConflictBanner
- **PURPOSE**: Red-flag alert card highlighting extent or boundary discrepancies across deeds.
- **PROPS**: `conflict: ConflictObj`, `onResolve: (decision: string) => void`.
- **STATES**: Active Red-Flag, Under Review, Resolved.
- **PERMISSIONS**: `LEAD_ADVOCATE`, `ASSOCIATE`.
- **ACCESSIBILITY**: `role="alert"`, high-contrast warning icon.
- **RESPONSIVE**: Stacked side-by-side comparison on smaller screens.

---

### 12. ReviewPanel
- **PURPOSE**: Human-in-the-loop verification sidebar for reviewing AI extractions.
- **PROPS**: `entity: EntityObj`, `onVerify: () => void`, `onEdit: (val: string) => void`, `onReject: () => void`.
- **STATES**: `AI EXTRACTION`, `HUMAN VERIFIED`, `REJECTED`.
- **PERMISSIONS**: `LEAD_ADVOCATE`, `ASSOCIATE`.
- **ACCESSIBILITY**: Form fields labeled; keyboard shortcuts (`Ctrl+Enter` to verify).
- **RESPONSIVE**: Slide-over drawer on tablet/mobile.

---

### 13. AuditEvent
- **PURPOSE**: Single event row display in audit log.
- **PROPS**: `timestamp: string`, `userName: string`, `action: string`, `resource: string`, `ip: string`.
- **STATES**: Default, Expanded Detail.
- **PERMISSIONS**: `LEAD_ADVOCATE`, `AUDITOR`.
- **ACCESSIBILITY**: Monospace font for IP and hashes; accessible table row semantics.
- **RESPONSIVE**: Collapses IP and details under expandable accordion on mobile.

---

### 14. DataTable
- **PURPOSE**: Reusable data table component with sorting, pagination, and filter capabilities.
- **PROPS**: `columns: ColumnDef[]`, `data: any[]`, `pagination: PaginationObj`.
- **STATES**: Loading, Rendered, Empty, Sorted.
- **PERMISSIONS**: All users.
- **ACCESSIBILITY**: Proper table semantics (`<th>`, `<td>`, `scope="col"`), keyboard sort triggers.
- **RESPONSIVE**: Horizontal scrolling with fixed left column.

---

### 15–20. Utility Primitives (EmptyState, ErrorState, ConfirmDialog, Toast, Progress, Modal)
- Standardized UI primitives with explicit props, keyboard traps (`FocusTrap`), `aria-modal`, and accessible color contrast.
