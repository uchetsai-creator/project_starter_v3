# Data Model

<!--
  Describes the database design.
  Corresponds to the technical implementation layer of business-objects.md.
  The state machine section includes both a text version and a state block.
  After writing, run: python3 docs/script/state_to_html.py docs/specs/data-model.md
-->

## [Entity Name] (`[table_name]`)

**Purpose:** [What this table stores]

| Field | Type | Constraint | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Primary key |
| `[field]` | VARCHAR(255) | NOT NULL | [Description] |
| `[field]` | TEXT | | [Description, nullable] |
| `[fk_field]_id` | UUID | FK → `[table].id`, NOT NULL | [Description] |
| `status` | ENUM | NOT NULL | See state machine below |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| `updated_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| `deleted_at` | TIMESTAMPTZ | | Soft delete |

**Indexes:**

| Index name | Field | Purpose |
|---|---|---|
| `idx_[table]_[field]` | `[field]` | [Which query this serves] |

**State Machine:**

```
[draft] → [active] → [completed]
              ↓
          [cancelled]
```

| State | Can transition to |
|---|---|
| `draft` | `active`, `cancelled` |
| `active` | `completed`, `cancelled` |
| `completed` | — |
| `cancelled` | — |

```state
title: [Entity Name] Status

[*] -> draft
draft -> active: [condition, e.g., admin approves]
draft -> cancelled: [condition, e.g., user cancels]
active -> completed: [condition, e.g., all items shipped]
active -> cancelled: [condition, e.g., admin cancels]
completed -> [*]
cancelled -> [*]
```

---

## [Entity Name] (`[table_name]`)

**Purpose:** [Description]

| Field | Type | Constraint | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Primary key |
| `[field]` | VARCHAR(255) | NOT NULL | [Description] |
| `[fk_field]_id` | UUID | FK → `[table].id`, NOT NULL | [Description] |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| `updated_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

**Indexes:**

| Index name | Field | Purpose |
|---|---|---|
| `idx_[table]_[fk]_id` | `[fk]_id` | Lookup by foreign key |

---

## Migration Plan

| Order | File name | Operation | Reversible |
|---|---|---|---|
| 1 | `[timestamp]_create_[table]` | CREATE TABLE | ✅ |
| 2 | `[timestamp]_create_[table]` | CREATE TABLE | ✅ |
| 3 | `[timestamp]_add_index_[table]` | CREATE INDEX | ✅ |
| 4 | `[timestamp]_modify_[col]_[table]` | ALTER TABLE | ⚠️ Verify data first |

---

## Query Patterns

| Query | Condition | Index used |
|---|---|---|
| [e.g., List all orders for a user] | `user_id = ?` AND `deleted_at IS NULL` | `idx_orders_user_id` |
| [Description] | `status = ?` | `idx_orders_status` |
