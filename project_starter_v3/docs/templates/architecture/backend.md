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
  Describes the backend module dependency structure.
  Fill in based on the actual stack and layer pattern described above.
  Use real layer names from your Stack and Layering sections above.
  e.g. if your stack uses Controller → Service → Repository, use those names.
       if your stack uses Handler → UseCase → Store, use those names instead.
  After writing, run: python3 docs/script/component_to_html.py docs/architecture/backend.md
-->

```component
title: Backend Module Structure

component "[e.g., Controller / Handler / Router]" as Layer1 {
  provides: [e.g., HTTP endpoints]
  requires: Layer2
}

component "[e.g., Service / UseCase / Domain]" as Layer2 {
  provides: [e.g., business logic]
  requires: Layer3
}

component "[e.g., Repository / Store / DAO]" as Layer3 {
  provides: [e.g., DB queries]
  requires: [e.g., Database]
}

Layer1 --> Layer2 : uses
Layer2 --> Layer3 : uses
```
