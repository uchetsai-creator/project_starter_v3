# AGENTS

## Project Initialization

If starting a new project:
1. Create docs/project-requirements.md from templates/project-requirements.md.
2. Create docs/specs/research.md from templates/specs/research.md (resolve all NEEDS CLARIFICATION).
3. Create docs/architecture/architecture.md from templates/architecture/architecture.md.
4. Create docs/architecture/backend.md, frontend.md, database.md, deployment.md from templates/architecture/.
5. Create docs/specs/data-model.md from templates/specs/data-model.md.
6. Create docs/specs/api-contract.md from templates/specs/api-contract.md.
7. Create docs/specs/permissions.md from templates/specs/permissions.md.
8. Create docs/project-plan.md from templates/project-plan.md.
9. Create docs/current-state.md from templates/current-state.md.

---

If continuing an existing project:
Read:
1. AGENTS.md
2. docs/current-state.md
3. Required Context only

Required Context should contain only the documents required to complete the Current Task.
Required Context Do not include:
- docs/project-plan.md
- docs/project-requirements.md
- docs/changelog.md

unless the task explicitly requires them.

Do not scan repository.

For planning rules (writing requirements, breaking down sprints/tasks), read docs/rules/planning-rules.md.
For what each document is for and when it changes, read docs/rules/document-purposes.md — reference only, not required every task.

---

## Development Principles

- Prefer maintainable architecture over temporary shortcuts
- Maintainability First
- Package First
- Glue Code
- Incremental Changes
- No Unrelated Refactor

---

## Package First

Priority:
1. Existing package
2. Existing utility
3. Framework convention
4. Custom code

Custom code only for:
- Business Logic
- Domain Rules
- Data Mapping
- System Integration

---

## Current State

docs/current-state.md is the active task.

Before starting work:
* Read docs/current-state.md.
* If Current Task exists:
  * Read Required Context.
  * Start implementation.
* Otherwise:
  * Read docs/project-plan.md.
  * Select the next incomplete task.
  * Update docs/current-state.md.
  * Start implementation.

After task completion:

1. Move Current Task to docs/changelog.md.
2. Mark the task completed in docs/project-plan.md.
3. Update docs/flows/module-data-flow.md with actual function names and file paths from the implementation.
4. Update docs/codebase-map.md with the files touched in this task, classified by layer (DB/BE/FE/MOD) and type (Package/Custom).
5. Run the Document Update Checklist below. For each item, check yes/no — do not skip the check.
6. Run the Module Completion Check below. Do not skip this check, even if the answer is usually "no."
7. Select the next incomplete task from docs/project-plan.md.
8. Update docs/current-state.md.
9. Update Required Context.

### Module Completion Check

Run this check after every task — most of the time the answer will be "no," but the check itself must not be skipped.

* Does completing this task finish all DB/BE/FE tasks for its module in docs/project-plan.md?
  * If no: this module is not yet complete. Skip the rest of this section.
  * If yes: this module is now complete. Do both of the following:
    1. Insert logger calls into the module's code, following the rules defined in docs/specs/logging-spec.md (required log points, message format, logger instantiation). Direct print/console statements are not allowed.
       logging-spec.md itself is the rule definition — do not add module-specific content to it.
       Create or update docs/flows/log-<module-name>.md (one file per module) to list every log point added, in call order.
    2. Ask: "Would you like to add debug instrumentation to this module? (follows debug-instrumentation-rules.md)"
       * If yes: follow debug-instrumentation-rules.md and instrument the module.
       * If no: continue.

### Document Update Checklist

Run through every item below after every task. This is mandatory, not optional.

- [ ] docs/specs/research.md — did this task involve a new technology decision, or resolve a NEEDS CLARIFICATION? If yes, update.
- [ ] docs/specs/quickstart.md — did setup steps, verification steps, or environment requirements change? If yes, update.
- [ ] docs/specs/data-model.md — did the schema, entities, relationships, or indexes change? If yes, update, then regenerate the ERD by running `python3 docs/script/schema_to_html.py <schema file>`.
- [ ] docs/specs/api-contract.md — were endpoints added/changed, or did error codes or validation rules change? If yes, update.
- [ ] docs/specs/permissions.md — were roles, the permission matrix, or API endpoints changed? If yes, update.
- [ ] docs/architecture/architecture.md — did components or data flows change? If yes, update, then regenerate the diagram by running `python3 docs/script/architecture_to_html.py docs/architecture/architecture.md`.
- [ ] docs/architecture/backend.md — did backend layering, stack, or module pattern change? If yes, update.
- [ ] docs/architecture/frontend.md — did frontend stack, page structure, or component strategy change? If yes, update.
- [ ] docs/architecture/database.md — did main entities or relationships change (conceptual level)? If yes, update.
- [ ] docs/architecture/deployment.md — did services, env vars, or build/deploy flow change? If yes, update.
- [ ] docs/specs/logging-spec.md Module Naming Convention table — does this task introduce a module name not yet listed? If yes, add one line (name + short description) to the table. Do not add module-specific logging detail here — that belongs in docs/flows/log-<module-name>.md.
- [ ] docs/business/business-rules.md — did business constraints or policies change? If yes, update.
- [ ] docs/business/business-objects.md — were business entities added or changed? If yes, update.
- [ ] docs/business/business-process.md — did the business workflow, decision points, or exceptions change? If yes, update.

For the full explanation of why each document updates on these triggers, see docs/rules/document-purposes.md.

---

## Task Completion

Return:
- Verification
