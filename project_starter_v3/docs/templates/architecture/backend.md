# architecture/backend.md

Purpose:
Describe backend structure.

Include:
- Stack
- Layering
- Layer responsibilities
- Module pattern

Avoid:
- Full API endpoint list
- Feature requirements
- Business rules

---

## Stack

[e.g., Node.js 22 / Express / Prisma / PostgreSQL]

## Layering

```
Controller → Service → Repository → Database
```

| Layer | Responsibility |
|---|---|
| Controller | HTTP request/response, input validation |
| Service | Business logic, orchestration |
| Repository | Database access, query abstraction |

## Module Pattern

[Describe the file structure for each feature, e.g.:]

```
src/
└── [module]/
    ├── [module].controller.ts
    ├── [module].service.ts
    └── [module].repository.ts
```

## Component Structure

<!--
  After writing, run: python3 docs/script/component_to_html.py docs/architecture/backend.md
-->

```component
title: Backend Module Structure

component "[Module A]" as ModA {
  provides: [method1, method2]
  requires: [Module B]
}

component "[Module B]" as ModB {
  provides: [method1]
  requires: Database
}

component "Database" as DB {
  provides: CRUD operations
  requires:
}

ModA --> ModB : uses
ModB --> DB : queries
```
