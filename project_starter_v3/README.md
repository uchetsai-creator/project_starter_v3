# Project Starter

A documentation-first template for AI-assisted development. Define what you're building before
an AI agent (Claude Code, etc.) starts writing code — then keep every doc in sync automatically
as work progresses.

This repo is a **pure template repository**. It contains no real project content — only blank
scaffolding under `templates/`. Copy `templates/` into a new project's `docs/` folder to start.

---

## How it works

1. **`AGENTS.md`** defines the rules an AI agent follows: which docs to create, when to update
   them, and what to do when a task or module completes.
2. **`templates/`** holds the blank scaffolding — every document the agent will fill in.
3. As work happens, the agent keeps `docs/` (in your actual project) in sync with what was built,
   following the checklist in `AGENTS.md`.

```
project_starter_v2_note-main/        ← this repo (template only)
├── AGENTS.md
├── debug-instrumentation-rules.md
└── templates/
    ├── project-requirements.md      ← project scope, goals, edge cases, acceptance criteria
    ├── project-plan.md              ← sprint/task breakdown (DB → BE → FE per feature)
    ├── current-state.md             ← the active task
    ├── changelog.md                 ← completed task history
    ├── codebase-map.md              ← package vs. custom code, by layer
    │
    ├── specs/
    │   ├── research.md              ← technology decisions + alternatives considered
    │   ├── quickstart.md            ← how to run and verify the project end-to-end
    │   ├── data-model.md            ← schema, indexes, state machines, migrations
    │   ├── api-contract.md          ← endpoints, validation rules, error codes
    │   ├── permissions.md           ← roles, RBAC matrix, endpoint access control
    │   └── logging-spec.md          ← logging rules + module naming convention
    │
    ├── architecture/
    │   ├── architecture.md          ← components, data flow, structured YAML for diagram
    │   ├── backend.md               ← backend stack, layering, module pattern
    │   ├── frontend.md              ← frontend stack, page structure, component strategy
    │   ├── database.md              ← entities/relationships (conceptual level)
    │   └── deployment.md            ← services, env vars, startup/build/deploy flow
    │
    ├── business/
    │   ├── business-process.md      ← high-level workflows, decision points, exceptions
    │   ├── business-objects.md      ← entities, relationships, status flow
    │   └── business-rules.md        ← approval/validation/notification/audit rules
    │
    ├── flows/
    │   ├── module-data-flow.md      ← index + rules for code-level flow files (per module)
    │   └── module-flow.md           ← detailed execution steps for a business process
    │
    └── script/
        ├── architecture_to_html.py  ← architecture.md → interactive HTML + static SVG
        ├── schema_to_html.py        ← Prisma/SQL schema → ERD (interactive HTML + static SVG)
        └── build_pdf.py             ← merges all of docs/ into one PDF, with diagrams embedded
```

When a new project starts, `templates/` is copied in and becomes `docs/` — see
[Project Initialization](#project-initialization) below.

---

## Project Initialization

A new project does **not** keep `templates/` — it copies each file into `docs/`, filling in the
placeholders as it goes:

```
new_project/
├── AGENTS.md
├── debug-instrumentation-rules.md
└── docs/
    ├── project-requirements.md
    ├── project-plan.md
    ├── current-state.md
    ├── changelog.md
    ├── codebase-map.md
    ├── specs/
    ├── architecture/
    ├── business/
    ├── flows/
    │   └── log-<module-name>.md     ← generated when each module is implemented
    └── script/
```

`AGENTS.md` drives this automatically — an AI agent starting a new project will create each file
from its matching template in order (requirements → research → architecture → data model →
API contract → permissions → plan → current state).

---

## Working on an existing project

The agent reads, in order:

1. `AGENTS.md`
2. `docs/current-state.md` — the active task
3. Only the docs the current task actually needs (it does **not** scan the whole repo)

After finishing a task, it works through a mandatory checklist (see `AGENTS.md` →
`Document Update Checklist`) — checking whether each spec/architecture/business doc needs
updating based on what just changed.

When a task finishes **all** DB/BE/FE work for a module, three more things happen automatically:

- Logger calls are inserted into the module's code (per `logging-spec.md`), and
  `docs/flows/log-<module-name>.md` is created/updated
- You're asked whether to add temporary debug instrumentation (per `debug-instrumentation-rules.md`)
- The merged documentation PDF is regenerated (`docs/project-documentation.pdf`)

---

## Diagrams

Two scripts turn structured Markdown into diagrams — each one outputs both an **interactive HTML**
(drag, zoom, click connections) and a **static SVG** (for screenshots / PDF embedding):

```bash
# System architecture — reads the YAML block inside architecture.md
python3 docs/script/architecture_to_html.py docs/architecture/architecture.md

# Database ERD — reads a Prisma schema or SQL DDL file
python3 docs/script/schema_to_html.py path/to/schema.prisma
```

Both produce `<name>.html` and `<name>.svg` side by side.

---

## Generating the merged PDF

Combines every real document under `docs/` (excluding `templates/` and `script/`) into a single
PDF — table of contents, page numbers, and any architecture/ERD diagrams embedded as images with
a clickable link to the original interactive HTML.

```bash
pip install markdown weasyprint cairosvg --break-system-packages
python3 docs/script/build_pdf.py docs -o docs/project-documentation.pdf
```

This runs automatically whenever a module completes (see above) — you don't need to ask for it,
but you can also run it manually any time.

---

## Key design decisions

- **Templates vs. docs**: `templates/` is always blank scaffolding. Real content only ever lives
  in a project's `docs/` folder, never in this repo.
- **Task granularity**: each task should be roughly half a day to one day of work, and
  independently completable as a single Current Task — see `docs/rules/planning-rules.md`
  (embedded in `AGENTS.md`).
- **Task ordering**: shared foundation first, then each feature as a vertical slice
  (DB → BE → FE), rather than completing all DB work before moving to BE.
- **Package First**: prefer an existing package, then an existing utility, then framework
  convention, and only write custom code for business logic, domain rules, data mapping, or
  system integration.
- **Incremental updates only**: `codebase-map.md` and `module-data-flow.md` are updated one task
  at a time — the agent never re-scans the whole repository to regenerate them.
