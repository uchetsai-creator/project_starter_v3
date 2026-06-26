# architecture/database.md

Purpose:
Describe the database at a conceptual level — what exists, how it relates, and why it was
designed this way. Field-level detail belongs in docs/specs/data-model.md.

Include:
- Database engine
- Main entities (3-5 sentences, no field lists)
- Key relationships
- Important constraints
- Schema decisions (why, not what)

Avoid:
- Full schema duplication
- Field-by-field listings
- API or UI details

---

## Database Engine

[e.g., PostgreSQL 16 / MySQL 8 / SQLite]

## Main Entities

[3-5 sentences describing the core entities and how they relate at a high level.
Do not list fields. Focus on what each entity represents and its role in the system.]

e.g., The system has five core entities: Equipment, Line, AlarmRule, AlarmEvent, and WorkOrder.
Equipment belongs to a Line. AlarmRules are configured per Equipment and trigger AlarmEvents
when thresholds are crossed. WorkOrders track production quantities against planned targets.

## Key Relationships

[List the most important relationships and their cardinality.]

- [Entity A] → [Entity B]: one-to-many ([reason])
- [Entity A] → [Entity B]: many-to-many (via [join table])

## Important Constraints

[List DB-level constraints that encode meaningful business rules.]

- [e.g., UNIQUE(lineId, stationType) on Equipment — each line can only have one station of each type]
- [e.g., quantity invariant: goodQuantity + defectQuantity ≤ actualQuantity ≤ plannedQuantity]

## Schema Decisions

[Explain non-obvious design choices — why UUID vs auto-increment, why soft delete,
why a particular denormalization, etc.]

- [e.g., UUID primary keys — avoids sequential ID leakage, supports future multi-tenant scenarios]
- [e.g., Soft delete (deletedAt) on [tables] — audit trail required, hard delete not permitted]
- [e.g., [Field] stored on [table] rather than computed — simplifies [service] without requiring a JOIN]
