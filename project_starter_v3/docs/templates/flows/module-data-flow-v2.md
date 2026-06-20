# module-data-flow.md

## Rules

* This file acts as the module flow index and rule definition.
* Do not put module flows in this file.
* Each module must have its own flow file.
* Each module flow file must follow the rules and format defined in this document.

### Implementation Flow Rules

* After implementation, update the matching module flow file with actual function names and file paths.
* If no matching implementation flow exists, create one.

### CRUD Rules

* Every module must have CRUD data flows.
* Create separate flows for:

  * Create
  * Read/List
  * Read Detail (if applicable)
  * Update
  * Delete (if applicable)
* If a CRUD operation is not supported, explicitly mark it as "Not Supported".

---

## Implementation Format

Feature Name
```
User Action
↓
Step Name
File: path/to/file
↓
Step Name
File: path/to/file
↓
Step Name
File: path/to/file
↓
...
↓
UI Update
File: path/to/file
```
Describe the actual execution order.

Common step types:

- Frontend Component
- Event Handler
- State Change
- Route Change
- Hook
- API
- Controller Method
- Service Method
- Repository Method
- Database Operation
- Response
- Cache Update
- Re-render
- UI Update

Only use the step types that exist for the feature.

---

## Module Flow Files

| Module | Files |
|---|---|
| [e.g., Order Create] | `docs/flows/order-create-flow.md` |
| [module] | [files] |
