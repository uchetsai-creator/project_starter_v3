# module-data-flow.md

## Rules

* This file acts as the module flow index and rule definition.
* Do not put module flows in this file.
* Each module must have its own flow file.
* Each module flow file must follow the rules and format defined in this document.

### Implementation Flow Rules

* After implementation, update the matching module flow file with actual function names and file paths.
* If no matching implementation flow exists, create one.
* Each module flow file must include a class block describing the code structure.
* After writing, run: python3 docs/script/class_to_html.py docs/modules/<module>/<module>-module-data-flow.md

### CRUD Rules

* Every module must have CRUD data flows.
* Create separate flows for:

  * Create
  * Read / List
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
...
↓
UI Update
File: path/to/file
```

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

## Class Structure Format

Each module flow file must also include a class block:

```class
title: [Module Name] Class Structure

class [Controller] {
  +[method](req, res): void
  +[method](req, res): void
}

class [Service] {
  +[method](input: [Type]): [ReturnType]
  -[privateMethod](param): [Type]
}

class [Repository] {
  +[method](id: string): [Type]
  +[method](input: [Type]): [Type]
}

[Controller] --> [Service]: uses
[Service] --> [Repository]: uses
```

---

## Module Flow Files

Each module has its own subfolder under `docs/modules/`.

Folder and file naming convention:
```
docs/modules/
├── module-data-flow.md          ← this index file
└── [module-name]/
    ├── [module-name]-module-data-flow.md
    └── log-[module-name].md
```

Examples:
```
docs/modules/order/order-module-data-flow.md
docs/modules/inventory/inventory-module-data-flow.md
docs/modules/payment/payment-module-data-flow.md
```

Files matching `*-module-data-flow.md` are automatically included in the PDF.

| Module | Folder | Flow file |
|---|---|---|
| [e.g., Order] | `docs/modules/order/` | `order-module-data-flow.md` |
| [module] | `docs/modules/[module]/` | `[module]-module-data-flow.md` |
