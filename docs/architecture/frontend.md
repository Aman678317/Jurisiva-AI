# Frontend Architecture Specification

## Framework & Tooling Stack
- **Framework**: React 18+ with TypeScript & Vite / Next.js shell.
- **Styling**: Tailored CSS tokens (`design-system-requirements.md`) with Tailwind CSS / CSS Modules.
- **State Management**: Zustand / React Context for UI state (active tab, viewer zoom, modal state); TanStack Query (React Query) for server data caching and sync.
- **PDF Viewer**: PDF.js canvas renderer with custom SVG bounding-box highlight overlay layer.

## Module & Folder Structure

```
apps/web/
 ├── src/
 │    ├── app/ (Routing & Page Layouts)
 │    ├── components/
 │    │    ├── ui/ (Reusable Primitives: Button, Input, Modal, Table)
 │    │    └── legal/ (Domain Components: DocumentViewer, PropertyTimeline, Citation)
 │    ├── features/
 │    │    ├── auth/
 │    │    ├── matters/
 │    │    ├── documents/
 │    │    ├── property/
 │    │    ├── copilot/
 │    │    └── reports/
 │    ├── lib/ (API client, token helpers, formatters)
 │    └── types/ (Shared TypeScript interfaces)
```

## Security Guardrail
No business-critical authorization or security logic relies on frontend code alone. All actions are authenticated and authorized by backend middleware.
