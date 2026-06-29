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

<!--
  State the actual database engine and version used.
  If the project uses multiple data stores, list all of them and what each is used for.

  Examples:
    PostgreSQL 16
    MySQL 8 / Redis 7 (cache)
    MongoDB 7
    SQLite 3
    DynamoDB
    Firebase Firestore
    Supabase (PostgreSQL)
    PlanetScale (MySQL-compatible)
    CockroachDB
    [no database — file-based / in-memory only]
-->

[Database engine and version]

---

## Main Entities

<!--
  3-5 sentences describing the core entities and how they relate at a high level.
  Do not list fields. Focus on what each entity represents and its role in the system.

  If the project uses a non-relational store (document DB, key-value, graph),
  describe the main collections, documents, or nodes instead of "entities".
-->

[Description of core entities / collections / nodes and how they relate]

---

## Key Relationships

<!--
  List the most important relationships and their cardinality.
  For relational DBs: one-to-many, many-to-many, etc.
  For document DBs: embedding vs. referencing decisions.
  For key-value stores: key namespace design.
  For graph DBs: node types and edge types.
-->

- [Entity / Collection A] → [Entity / Collection B]: [relationship type and reason]
- [Entity / Collection A] → [Entity / Collection C]: [relationship type and reason]

---

## Important Constraints

<!--
  List only constraints that are non-obvious or encode a meaningful business rule
  that would not be self-evident from reading the schema.

  Do NOT repeat field-level constraints already visible in data-model.md
  (e.g. NOT NULL, FK references, basic UNIQUE on a single column).
  Those belong in data-model.md — not here.

  What belongs here:
  - Multi-column UNIQUE constraints that encode a business rule
    e.g. UNIQUE(lineId, stationType) — each line can only have one station of each type
  - CHECK constraints that encode a business invariant
    e.g. goodQuantity + defectQuantity ≤ actualQuantity
  - Cross-entity rules enforced at the DB level
  - For document DBs: schema validation rules or index uniqueness with business significance
  - Omit this section entirely if nothing meets this bar
-->

- [Constraint and the business rule it enforces]

---

## Schema Decisions

<!--
  Explain non-obvious design choices — why this ID type, why this storage approach,
  why a particular denormalization, etc.

  Examples for relational:
    UUID primary keys — avoids sequential ID leakage, supports future multi-tenant scenarios
    Soft delete (deletedAt) on [tables] — audit trail required, hard delete not permitted
    [Field] stored on [table] rather than computed — simplifies queries without requiring a JOIN

  Examples for document DB:
    Orders embed OrderItems — items are always read with the order, never independently
    Users reference Addresses — addresses are shared across multiple entities

  Examples for key-value:
    Session keys use TTL of 24h — matches auth token expiry
    User profile cached separately from preferences — different invalidation patterns
-->

- [Decision and rationale]
