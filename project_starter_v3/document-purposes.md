# Document Purposes

<!--
  Reference only. Not read every task.
  The mandatory per-task update check lives in AGENTS.md → Document Update Checklist.
  This file explains WHY and details each document's purpose, update triggers, and
  which diagram script to run after updating.
-->

## Specs (docs/specs/)

### research.md
Update when:
* New technology decisions are made
* NEEDS CLARIFICATION items are resolved
* Architecture decisions change

### quickstart.md
Update when:
* Setup steps change
* New verification steps are added
* Environment requirements change

### data-model.md
Update when:
* Schema changes
* New entities are added
* Relationships change
* Indexes are added or removed

After updating, regenerate both diagrams:
* ERD: `python3 docs/script/schema_to_html.py <schema file>`
* State diagram: `python3 docs/script/state_to_html.py docs/specs/data-model.md`

### api-contract.md
Update when:
* New endpoints are added
* Request/response format changes
* Error codes are added
* Validation rules change

### permissions.md
Update when:
* New roles are added
* Permission matrix changes
* New endpoints are added to API contract
* New features are added to the system

After updating, regenerate use case diagram:
`python3 docs/script/usecase_to_html.py docs/specs/permissions.md`

The use case diagram is a **system-level view** — it lists ALL roles and ALL major
functions across all modules in one diagram, not per resource or per module.

### logging-spec.md
Purpose:
Define logging rules, format, and module naming conventions.
All modules must follow this spec.

Update when:
* New modules are added (add one line to the Module Naming Convention table)
* Log format changes

This file is the rule definition only — do not add module-specific logging content here.
Module-specific log points live in docs/flows/log-<module-name>.md.

---

## Architecture (docs/architecture/)

### architecture.md
Purpose:
Describe system component overview and data flow.
Holds the structured YAML block used by architecture_to_html.py to generate the diagram.

Update when:
* New components are added
* Data flows change
* Integration changes

After updating, regenerate diagram:
`python3 docs/script/architecture_to_html.py docs/architecture/architecture.md`

### backend.md
Purpose:
Describe backend structure — stack, layering, layer responsibilities, module pattern.
Includes a component block for the backend module structure diagram.

Update when:
* Backend layering, stack, or module pattern changes

After updating, regenerate component diagram:
`python3 docs/script/component_to_html.py docs/architecture/backend.md`

### frontend.md
Purpose:
Describe frontend structure — stack, page structure, component strategy, API hook strategy.
Includes a component block for the frontend module structure diagram.

Update when:
* Frontend stack, page structure, or component strategy changes

After updating, regenerate component diagram:
`python3 docs/script/component_to_html.py docs/architecture/frontend.md`

### database.md
Purpose:
Describe database structure at the conceptual level — main entities, main relationships,
important constraints. Not a field-by-field schema; that level of detail belongs in
docs/specs/data-model.md.

Update when:
* Main entities or relationships change

### deployment.md
Purpose:
Describe runtime structure — services, environment variables, local startup flow,
build/deploy flow.

Update when:
* Services, env vars, or build/deploy flow changes

---

## Flows (docs/modules/)

### module-data-flow.md
Purpose:
Index and rule definition for module-level code flows. Sits at `docs/modules/module-data-flow.md`.
Each module gets its own subfolder (`docs/modules/[module]/`) with its own flow file.

Update when:
* A new module is created — add a row to the Module Flow Files table

### [module]-module-data-flow.md
Purpose:
Track code-level execution flow (function names, file paths) for a specific module.
Also includes a class block describing the module's class/service structure.

Location: `docs/modules/[module]/[module]-module-data-flow.md`
Examples: `docs/modules/order/order-module-data-flow.md`

Files matching this pattern are automatically included in the PDF.

Update when:
* Function names or file paths change for this module
* A new CRUD operation is implemented
* The module's class structure changes

After updating, regenerate class diagram:
`python3 docs/script/class_to_html.py docs/modules/<module>/<module>-module-data-flow.md`

### [module]-flow.md
Purpose:
Describe cross-module service call sequences for a specific process.
Includes a Sequence Diagram showing which service calls which service in what order.
Business steps and decision branches belong in docs/business/business-process.md.

Location: `docs/modules/[module]/[module]-flow.md`
Example: `docs/modules/order/order-flow.md`

Update when:
* Cross-module service calls change
* A new cross-module process is added

After updating, regenerate sequence diagram:
`python3 docs/script/sequence_to_html.py docs/modules/<module>/<module>-flow.md`

### log-<module-name>.md
Purpose:
Track every log point in a module, in call order. One file per module.
Not included in the PDF — this is an implementation detail reference for developers.

Location: `docs/modules/[module]/log-[module].md`
Generate when the module is complete (see AGENTS.md → Module Completion Check).
Update immediately if function names or file paths change.

---

## Business (docs/business/)

### business-process.md
Purpose:
Index file listing all business process documents.
Each business process has its own dedicated file: `docs/business/[process-name]-process.md`.

Update when:
* A new business process file is created — add a row to the table

### [process-name]-process.md
Purpose:
Describe one business process — goal, steps, decision points, exceptions, and Activity Diagram.
Cross-module technical call sequences belong in docs/modules/[module]/[module]-flow.md.

Location: `docs/business/[process-name]-process.md`
Examples: `order-create-process.md`, `order-cancel-process.md`

Files matching `*-process.md` are automatically included in the PDF.

Update when:
* The business workflow, decision points, or exceptions change

After updating, regenerate activity diagram:
`python3 docs/script/activity_to_html.py docs/business/[process-name]-process.md`

### business-objects.md
Purpose:
Index and rule definition for all business object documents.
Each business object has its own file: `docs/business/[object-name]-object.md`.

Update when:
* A new business object file is created — add a row to the table
* A relationship between objects changes — update the Relationships table

### [object-name]-object.md
Purpose:
Describe one business entity — who owns it, who creates it, its lifecycle, and its
business-level state machine. Technical field-level detail belongs in docs/specs/data-model.md.

Location: `docs/business/[object-name]-object.md`
Examples: `order-object.md`, `inventory-object.md`

Files matching `*-object.md` are automatically included in the PDF.

Update when:
* The business entity's description, ownership, or lifecycle changes
* Status transitions or responsible roles change

After updating, regenerate state diagram:
`python3 docs/script/state_to_html.py docs/business/[object-name]-object.md`

### business-rules.md
Purpose:
Describe business constraints and policies — approval rules, validation rules,
notification rules, audit rules.

Update when:
* Business rules change

---

## Root-level (docs/)

### current-state.md
Purpose:
The active task. Read first when continuing an existing project.

### changelog.md
Purpose:
Completed task history. Current Task moves here once finished.

### codebase-map.md
Purpose:
Track which files are package usage vs custom logic, classified by layer (DB/BE/FE/MOD).
Used to verify the Package First principle is being followed.

Update when:
* A task is completed — add the files touched in that task.

Do not scan the entire repository to regenerate this file. Update incrementally, one task at a time.

---

## Diagram Scripts Reference

| Script | Input format | Output suffix | Embedded in |
|---|---|---|---|
| `architecture_to_html.py` | yaml block in architecture.md | `.html` / `.svg` | `architecture/architecture.md` |
| `schema_to_html.py` | Prisma / SQL file | `.html` / `.svg` | `specs/data-model.md` |
| `state_to_html.py` | state block in any .md | `-state.html` / `.svg` | `specs/data-model.md`, `business/*-object.md` |
| `usecase_to_html.py` | usecase block in any .md | `-usecase.html` / `.svg` | `specs/permissions.md` |
| `activity_to_html.py` | activity block in any .md | `-activity.html` / `.svg` | `business/*-process.md` |
| `sequence_to_html.py` | sequence block in any .md | `-sequence.html` / `.svg` | `modules/*/` flow files |
| `class_to_html.py` | class block in any .md | `-class.html` / `.svg` | `modules/*/*-module-data-flow.md` |
| `component_to_html.py` | component block in any .md | `-component.html` / `.svg` | `backend.md` / `frontend.md` |
