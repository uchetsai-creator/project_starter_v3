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

After updating, regenerate use case diagram:
`python3 docs/script/usecase_to_html.py docs/specs/permissions.md`

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

### module-flow.md
Purpose:
Describe detailed execution steps for a business process, when business-process.md is not
granular enough. Sits at `docs/modules/module-flow.md` (shared) or create a dedicated
`docs/modules/[module]/[module]-flow.md` for a specific module's flow.
Includes both an activity block (execution steps) and a sequence block (cross-service calls).

Update when:
* A business process requiring operational detail is added or changes
* Cross-service call sequence changes

After updating, regenerate both diagrams:
* Activity: `python3 docs/script/activity_to_html.py <flow-file>`
* Sequence: `python3 docs/script/sequence_to_html.py <flow-file>`

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
Describe high-level business workflows — goal, process steps, decision points, exceptions,
pain points. Detailed execution steps belong in docs/flows/module-flow.md.

Update when:
* The business workflow, decision points, or exceptions change

### business-objects.md
Purpose:
Describe business entities, their relationships, and status flow (including lifecycle
sequence if statuses have a fixed order).

Update when:
* Business entities are added or changed

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
| `state_to_html.py` | state block in any .md | `-state.html` / `.svg` | `specs/data-model.md` |
| `usecase_to_html.py` | usecase block in any .md | `-usecase.html` / `.svg` | `specs/permissions.md` |
| `activity_to_html.py` | activity block in any .md | `-activity.html` / `.svg` | `modules/*/` flow files |
| `sequence_to_html.py` | sequence block in any .md | `-sequence.html` / `.svg` | `modules/*/` flow files |
| `class_to_html.py` | class block in any .md | `-class.html` / `.svg` | `modules/*/*-module-data-flow.md` |
| `component_to_html.py` | component block in any .md | `-component.html` / `.svg` | `backend.md` / `frontend.md` |
