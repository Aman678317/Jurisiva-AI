# Chapter 3 — Navigation Model & Responsive Behavior

## Navigation Architecture

### 1. Primary Global Navigation (Left Sidebar / Top Header)
- **Logo & Brand**: Branding element returning user to Organization Dashboard.
- **Matter Switcher Dropdown**: Allows fast switching between active matters without returning to root.
- **Global Items**:
  - `Matters` (Default active view)
  - `Global Search` (Cmd+K / Ctrl+K shortcut)
  - `Team & Settings`
  - `User Profile / Logout`

### 2. Secondary Matter Navigation (Sub-Header Tabs)
When inside a specific Matter Workspace, a persistent sub-header displays Matter ID, Client Name, and 7 navigation tabs:
1. `Overview`
2. `Documents`
3. `Evidence & Search`
4. `Property Intelligence`
5. `Copilot / Research`
6. `Reports`
7. `Audit Log`

### 3. Breadcrumbs & Context Tracking
- Format: `Organization Name` / `Matter Title (Survey #42/1)` / `Document Viewer (Sale Deed 1985)`
- Always visible at top of viewport to preserve matter context.

---

## Responsive Device Behavior

| Screen Size | Navigation & Workspace Layout Strategy |
| :--- | :--- |
| **Desktop (>= 1280px)** | **Primary Professional Workspace**. Full left sidebar, 7 sub-tabs, 3-column split view (Left: Context/Nav, Center: PDF Viewer, Right: Citations/AI Assistant). |
| **Tablet (768px – 1279px)** | Collapsible left sidebar (icon-only mode); Sub-tabs convert to horizontally scrollable tab bar; Right citation panel converts to slide-over drawer. |
| **Mobile (< 768px)** | Mobile drawer menu; Single-column view focusing on Matter Status, Document List, and Copilot Q&A. Split-screen PDF viewer shows warning banner recommending desktop for detailed boundary inspection. |
