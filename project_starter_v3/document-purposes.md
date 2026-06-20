# Document Purposes

<!--
  Reference only. Not read every task.
  The mandatory per-task update check lives in AGENTS.md → Document Update Checklist.
  This file explains WHY and details each document's purpose and update triggers.
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

Regenerate the ERD after updating, by running docs/script/schema_to_html.py.

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
Holds the structured YAML block used by docs/script/architecture_to_html.py to generate the diagram.

Update when:
* New components are added
* Data flows change
* Integration changes

Regenerate the diagram after updating, by running docs/script/architecture_to_html.py.

### backend.md
Purpose:
Describe backend structure — stack, layering, layer responsibilities, module pattern.

Update when:
* Backend layering, stack, or module pattern changes

### frontend.md
Purpose:
Describe frontend structure — stack, page structure, component strategy, API hook strategy.

Update when:
* Frontend stack, page structure, or component strategy changes

### database.md
Purpose:
Describe database structure at the conceptual level — main entities, main relationships, important constraints.
Not a field-by-field schema; that level of detail belongs in docs/specs/data-model.md.

Update when:
* Main entities or relationships change

### deployment.md
Purpose:
Describe runtime structure — services, environment variables, local startup flow, build/deploy flow.

Update when:
* Services, env vars, or build/deploy flow changes

---

## Flows (docs/flows/)

### module-data-flow.md
Purpose:
Index and rule definition for module-level code flows. Each module gets its own flow file following
the CRUD rules and implementation format defined here.

Update when:
* A module is implemented — update the corresponding flow file with actual function names and file paths

### module-flow.md
Purpose:
Describe detailed execution steps for a business process, when business-process.md isn't granular enough.

Update when:
* A business process requiring operational detail is added or changes

### log-<module-name>.md
Purpose:
Track every log point in a module, in call order. One file per module.

Generate when the module is complete (see AGENTS.md → Module Completion Check).
Update immediately if function names or file paths change.

---

## Business (docs/business/)

### business-process.md
Purpose:
Describe high-level business workflows — goal, process steps, decision points, exceptions, pain points.
Detailed execution steps belong in docs/flows/module-flow.md.

Update when:
* The business workflow, decision points, or exceptions change

### business-objects.md
Purpose:
Describe business entities, their relationships, and status flow (including lifecycle sequence
if statuses have a fixed order).

Update when:
* Business entities are added or changed

### business-rules.md
Purpose:
Describe business constraints and policies — approval rules, validation rules, notification rules, audit rules.

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
