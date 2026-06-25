# Codebase Map

<!--
  Location: templates/codebase-map.md
  Tracks which layer each file belongs to, and whether it is package usage or custom logic.
  Update incrementally after each task is completed.
  Do not scan the entire repository.

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

## Project Structure

<!--
  Fill in your actual project file/folder structure below.
  Include both source code and template/doc folders.
-->

```
project-root/
├── templates/                        ← planning & spec docs
│   ├── codebase-map.md
│   └── ...
│
├── [your-source-folder]/             ← e.g., src/ app/ backend/ frontend/
│   ├── [module-a]/
│   │   ├── [file]
│   │   └── [file]
│   └── [module-b]/
│       ├── [file]
│       └── [file]
│
├── [config files]                    ← e.g., package.json, prisma/, docker-compose.yml
└── ...
```

---

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
| `[file path]` | DB | Custom | |
| `[file path]` | BE | Custom | |
| `[file path]` | FE | Custom | |

---
