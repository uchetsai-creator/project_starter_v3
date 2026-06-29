# Project Starter

> **Repo structure note:** This repo should be cloned so that `AGENTS.md` sits at the
> root — i.e. `project_starter/AGENTS.md`, not `project_starter/project_starter/AGENTS.md`.
> If you see a doubled folder after cloning, move the contents up one level.

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
project_starter/                     ← this repo (template only)
├── AGENTS.md
├── debug-instrumentation-rules.md
├── code-quality-check.md            ← code review checklist for retrofitting existing projects
├── document-purposes.md             ← reference for what each document is for and when it changes
└── templates/
    ├── project-requirements.md      ← project scope, goals, edge cases, acceptance criteria
    ├── project-plan.md              ← sprint/task breakdown per feature
    ├── current-state.md             ← the active task
    ├── changelog.md                 ← completed task history
    ├── codebase-map.md              ← package vs. custom code, by layer; includes project tree
    │
    ├── specs/                        ← includes quickstart.md, research.md, data-model.md, etc.
    │   ├── quickstart.md            ← setup steps, prerequisites, local startup, verification
    │   ├── research.md              ← technology decisions + alternatives considered
    │   ├── data-model.md            ← schema, indexes, state machines, migrations
    │   ├── api-contract.md          ← endpoints, validation rules, error codes
    │   ├── permissions.md           ← roles, permission matrix, endpoint access control
    │   └── logging-spec.md          ← logging rules, logger instantiation, module naming
    │
    ├── architecture/
    │   ├── architecture.md          ← components, data flow, structured YAML for diagram
    │   ├── backend.md               ← backend stack, layering, module pattern (architecture-agnostic)
    │   ├── frontend.md              ← frontend stack, page structure, component strategy
    │   ├── database.md              ← entities/relationships (conceptual level)
    │   └── deployment.md            ← services, env vars, startup flow, verification steps
    │
    ├── business/
    │   ├── business-process.md      ← index + rules for business process files (per process)
    │   ├── business-objects.md      ← index + rules for business object files (per object)
    │   └── business-rules.md        ← approval/validation/notification/audit rules
    │
    ├── modules/
    │   ├── module-data-flow.md      ← index + rules for module flow files (Feature / Background Job / Shared Utility)
    │   └── module-flow.md           ← index + rules for cross-module sequence files (per module)
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
        ├── scan_codebase.py         ← scans src/ and reports which modules are undocumented
        ├── translate_docs.py        ← translate docs/ to Traditional Chinese → docs-zh/
        ├── build_pdf.py             ← merges all of docs/ into one PDF, with diagrams embedded
        └── pdf_allowlist.py         ← single source of truth for which files appear in the PDF
```

When a new project starts, `templates/` is copied in and becomes `docs/` — see
[Project Initialization](#project-initialization) below.

> **Note on file naming:** template files in this repo do not carry version suffixes
> (e.g. `module-data-flow.md`, not `module-data-flow-v2.md`). Version history is tracked
> in `CHANGELOG.md` at the repo root. When copying templates into a new project's `docs/`,
> use the base filename without any suffix.

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
    │   ├── business-process.md            ← index
    │   ├── [process-name]-process.md      ← one per business process, auto-included in PDF
    │   ├── business-objects.md            ← index
    │   ├── [object-name]-object.md        ← one per business object, auto-included in PDF
    │   └── business-rules.md
    ├── modules/
    │   ├── module-data-flow.md            ← index file
    │   ├── module-flow.md                 ← index file
    │   └── [module-name]/                 ← one subfolder per module (Feature or Background Job)
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

When a task finishes **all** work for a module, three more things happen automatically:

- Logger calls are inserted into the module's code (per `logging-spec.md`), and
  `docs/modules/[module]/log-[module].md` is created/updated
- You're asked whether to add temporary debug instrumentation (per `debug-instrumentation-rules.md`)
- The English PDF is regenerated (`docs/project-documentation-en.pdf`)

---

## Retrofitting an existing project

If a project already has code but no documentation, use the retrofit flow in `AGENTS.md`
(`If retrofitting an existing project`). The flow has five steps:

1. **Read the codebase** — entry point, schema, one complete module
2. **Run the module inventory scan** — `scan_codebase.py` lists every source folder and flags which
   are undocumented. You confirm the list before any documentation is written, so nothing gets missed
3. **Code Quality Check** — the agent runs `code-quality-check.md` and produces a report
   covering layering, Package First violations, naming, schema design, security, and error
   handling. You decide whether to fix issues first or document the codebase as-is
4. **Fill in architecture and spec documents** — describe what actually exists, not what should exist.
   Templates are architecture-agnostic — use your actual layer names, not assumed patterns
5. **Fill in module flow files** — one module at a time. Each module is classified as
   Feature, Background Job, or Shared Utility — each type has its own flow format
6. **Fill in project status** — reconstruct requirements, mark existing modules as completed in
   project-plan.md, generate the PDF

`code-quality-check.md` can also be used independently at any time as a standalone code review checklist.

---

## Module types

`module-data-flow.md` supports three module types, each with its own flow format:

| Type | Description | Entry point |
|---|---|---|
| **Feature** | Handles requests or commands — HTTP, GraphQL, CLI, RPC, WebSocket, etc. | Request / command |
| **Background Job** | Runs outside the request cycle — queue consumer, cron, event handler, worker | Queue message / schedule / event |
| **Shared Utility** | No entry point — called by other modules | None (class block only) |

The flow format does not prescribe layer names. Use whatever names your architecture actually has
(Controller, Handler, UseCase, Resolver, Model, etc.).

---

## Diagrams

Eight scripts turn structured Markdown blocks into diagrams — each outputs both an **interactive HTML**
(drag, zoom, click) and a **static SVG** (for PDF embedding). All UML scripts automatically
append a type suffix to the output filename to avoid collisions (e.g. `data-model-state.html`).

| Script | Input | Diagram type | Where it's embedded |
|---|---|---|---|
| `architecture_to_html.py` | `architecture.md` (yaml block) | System architecture | `architecture/architecture.md` |
| `schema_to_html.py` | Prisma / SQL file | ERD | `specs/data-model.md` |
| `state_to_html.py` | any `.md` (state block) | State machine | `specs/data-model.md`, `business/*-object.md` |
| `usecase_to_html.py` | any `.md` (usecase block) | Use case | `specs/permissions.md` |
| `activity_to_html.py` | any `.md` (activity block) | Activity flow | `business/*-process.md` |
| `sequence_to_html.py` | any `.md` (sequence block) | Sequence | `modules/[module]/[module]-flow.md` |
| `class_to_html.py` | any `.md` (class block) | Class structure | `modules/[module]/*-module-data-flow.md` |
| `component_to_html.py` | any `.md` (component block) | Component | `backend.md` / `frontend.md` |

```bash
# Examples
python3 docs/script/architecture_to_html.py docs/architecture/architecture.md
python3 docs/script/schema_to_html.py path/to/schema.prisma
python3 docs/script/state_to_html.py docs/specs/data-model.md
python3 docs/script/state_to_html.py docs/business/order-object.md
python3 docs/script/usecase_to_html.py docs/specs/permissions.md
python3 docs/script/activity_to_html.py docs/business/order-create-process.md
python3 docs/script/sequence_to_html.py docs/modules/order/order-flow.md
python3 docs/script/class_to_html.py docs/modules/order/order-module-data-flow.md
python3 docs/script/component_to_html.py docs/architecture/backend.md
```

---

## Module inventory scan

Before documenting an existing codebase, run the inventory scan to get an objective view of
what exists and what is already documented:

```bash
# Show tree view + coverage report
python3 docs/script/scan_codebase.py src

# Update the Project Structure and Coverage Summary sections in codebase-map.md automatically
python3 docs/script/scan_codebase.py src --update docs/codebase-map.md
```

The scan detects folder names to classify folders as Feature, Background Job, or
Shared/Infrastructure. Re-run at the end of Step 3 (retrofit) to confirm full coverage.

---

## Generating the merged PDF

Combines every real document under `docs/` (per the allowlist in `pdf_allowlist.py`) into a
single PDF — table of contents, page numbers, and diagrams embedded as images
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

To add a new document to the PDF, add it to **`docs/script/pdf_allowlist.py`** only —
`build_pdf.py` and `translate_docs.py` both import from it automatically. Note that
`business/*-process.md`, `business/*-object.md`, and `modules/*/*-module-data-flow.md`
are auto-scanned and do not need to be added manually.

---

## Key design decisions

- **Templates vs. docs**: `templates/` is always blank scaffolding. Real content only ever lives
  in a project's `docs/` folder, never in this repo.
- **Architecture-agnostic templates**: `backend.md`, `module-data-flow.md`, and `logging-spec.md`
  do not assume any specific layering pattern or language. Use your actual layer names and
  logger API — the templates provide structure, not prescription.
- **Module inventory before documentation**: the retrofit flow requires running `scan_codebase.py`
  and getting user confirmation before any documentation is written — so undocumented modules
  are caught at the start, not discovered at the end.
- **Three module types**: Feature (request-driven), Background Job (event/schedule-driven), and
  Shared Utility (no entry point). Each has its own flow format in `module-data-flow.md`.
- **Single PDF allowlist**: `pdf_allowlist.py` is the only file to edit when adding documents
  to the PDF. Both `build_pdf.py` and `translate_docs.py` import from it.
- **Task granularity**: each task should be roughly half a day to one day of work, and
  independently completable as a single Current Task — planning rules are defined directly in `AGENTS.md`.
- **Package First**: prefer an existing package, then an existing utility, then framework
  convention, and only write custom code for business logic, domain rules, data mapping, or
  system integration.
- **Incremental updates only**: `codebase-map.md` and `modules/module-data-flow.md` are updated one task
  at a time — the agent never re-scans the whole repository to regenerate them.
