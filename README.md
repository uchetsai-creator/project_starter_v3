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
project_starter_v3/                  ← this repo (template only)
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
    ├── modules/
    │   ├── module-data-flow.md      ← index + rules for code-level flow files (per module)
    │   └── module-flow.md           ← detailed execution steps for a business process
    │
    └── script/
        ├── architecture_to_html.py  ← architecture.md → interactive HTML + static SVG
        ├── schema_to_html.py        ← Prisma/SQL schema → ERD (interactive HTML + static SVG)
        ├── sequence_to_html.py      ← sequence diagram block → interactive HTML + static SVG
        ├── state_to_html.py         ← state diagram block → interactive HTML + static SVG
        ├── class_to_html.py         ← class diagram block → interactive HTML + static SVG
        ├── usecase_to_html.py       ← use case diagram block → interactive HTML + static SVG
        ├── activity_to_html.py      ← activity diagram block → interactive HTML + static SVG
        ├── component_to_html.py     ← component diagram block → interactive HTML + static SVG
        ├── translate_docs.py        ← translate docs/ to Traditional Chinese → docs-zh/
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
    ├── modules/
    │   ├── module-data-flow.md            ← index file
    │   ├── module-flow.md                 ← shared process flow template
    │   └── [module-name]/                 ← one subfolder per module
    │       ├── [module]-module-data-flow.md  ← auto-included in PDF
    │       └── log-[module].md               ← not in PDF, dev reference only
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
  `docs/modules/[module]/log-[module].md` is created/updated
- You're asked whether to add temporary debug instrumentation (per `debug-instrumentation-rules.md`)
- The English PDF is regenerated (`docs/project-documentation-en.pdf`)

---

## Diagrams

Eight scripts turn structured Markdown blocks into diagrams — each outputs both an **interactive HTML**
(drag, zoom, click) and a **static SVG** (for PDF embedding). All six UML scripts automatically
append a type suffix to the output filename to avoid collisions (e.g. `data-model-state.html`).

| Script | Input | Diagram type | Where it's embedded |
|---|---|---|---|
| `architecture_to_html.py` | `architecture.md` (yaml block) | System architecture | `architecture/architecture.md` |
| `schema_to_html.py` | Prisma / SQL file | ERD | `specs/data-model.md` |
| `state_to_html.py` | any `.md` (state block) | State machine | `specs/data-model.md` |
| `usecase_to_html.py` | any `.md` (usecase block) | Use case | `specs/permissions.md` |
| `activity_to_html.py` | any `.md` (activity block) | Activity flow | `modules/*/` flow files |
| `sequence_to_html.py` | any `.md` (sequence block) | Sequence | `modules/*/` flow files |
| `class_to_html.py` | any `.md` (class block) | Class structure | `modules/*/*-module-data-flow.md` |
| `component_to_html.py` | any `.md` (component block) | Component | `backend.md` / `frontend.md` |

```bash
# Examples
python3 docs/script/architecture_to_html.py docs/architecture/architecture.md
python3 docs/script/schema_to_html.py path/to/schema.prisma
python3 docs/script/state_to_html.py docs/specs/data-model.md
python3 docs/script/usecase_to_html.py docs/specs/permissions.md
python3 docs/script/activity_to_html.py docs/modules/order/order-module-flow.md
python3 docs/script/sequence_to_html.py docs/modules/order/order-module-flow.md
python3 docs/script/class_to_html.py docs/modules/order/order-module-data-flow.md
python3 docs/script/component_to_html.py docs/architecture/backend.md
```

---

## Generating the merged PDF

Combines every real document under `docs/` (per the explicit allowlist in `build_pdf.py`) into a
single PDF — table of contents, page numbers, and architecture/ERD diagrams embedded as images
with a clickable link to the original interactive HTML.

```bash
pip install markdown weasyprint cairosvg --break-system-packages

# English PDF (runs automatically when a module completes)
python3 docs/script/build_pdf.py docs --lang en -o docs/project-documentation-en.pdf

# Chinese PDF (manual, only when needed)
python3 docs/script/translate_docs.py docs --out docs-zh
python3 docs/script/build_pdf.py docs-zh --lang zh -o docs/project-documentation-zh.pdf
```

`translate_docs.py` translates every allowlisted markdown file to Traditional Chinese using
Google Translate (free, no API key needed), preserving code blocks, inline code, HTML comments,
and table structure. It mirrors the translated files into `docs-zh/`, which `build_pdf.py` then
reads exactly like `docs/`.

> Translation quality is good for headings and short sentences. Technical jargon and proper nouns
> may need manual review after translation.

To add a new document to the PDF, add it to `PDF_ALLOWLIST` in **both** `build_pdf.py` and
`translate_docs.py` — they each maintain their own copy of the list.

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
- **Incremental updates only**: `codebase-map.md` and `modules/module-data-flow.md` are updated one task
  at a time — the agent never re-scans the whole repository to regenerate them.
