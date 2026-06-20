# Codebase Map

<!--
  Tracks which layer each file belongs to, and whether it is package usage or custom logic.
  Update incrementally after each task is completed.
  Do not scan the entire repository.
-->

## [Feature / Module Name]

| File | Layer | Type | Description |
|---|---|---|---|
| `[file path]` | DB | Custom | [e.g., Order schema migration] |
| `[file path]` | BE | Custom | [e.g., Order business logic] |
| `[file path]` | BE | Package | [e.g., Express router] |
| `[file path]` | FE | Custom | [e.g., Order list page component] |
| `[file path]` | FE | Package | [e.g., React Query data fetching] |
| `[file path]` | MOD | Custom | [e.g., Cross-layer order state machine] |

---

## [Feature / Module Name]

| File | Layer | Type | Description |
|---|---|---|---|

---

<!--
  Type must be: Package / Custom
  Layer must be: DB / BE / FE / MOD

  Custom code should only appear in the following contexts
  (per the Package First principle in AGENTS.md):
  - Business Logic
  - Domain Rules
  - Data Mapping
  - System Integration

  If a Custom entry does not fall into one of these four contexts,
  flag it for review — it may be replaceable with a package.
-->
