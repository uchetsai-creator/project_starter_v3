# Business Objects Index

<!--
  This file is the index and rule definition for all business object documents.
  Each business object has its own dedicated file under docs/business/.
  Each object file must follow the rules and format defined in this document.

  Naming convention: [object-name]-object.md
  Location: docs/business/[object-name]-object.md
  Examples:
    docs/business/order-object.md
    docs/business/inventory-object.md
    docs/business/payment-object.md

  Files matching *-object.md are automatically included in the PDF.
  After writing a new object file, run:
  python3 docs/script/state_to_html.py docs/business/[object-name]-object.md
-->

---

## Rules

* This file acts as the index and rule definition.
* Do not put object content in this file.
* Each business object must have its own file.
* Each object file must follow the rules and format defined in this document.

### Content Rules

* Describe the business entity at the business level — not the database schema.
* Focus on who owns it, who creates it, who uses it, and its lifecycle.
* Technical field-level detail belongs in docs/specs/data-model.md — not here.

### Configuration Entity Exception

Not every entity in data-model.md needs its own `*-object.md` file. Skip it for entities that are:

* **Configuration / seed data** — created at deploy time, not by users during normal operation
  (e.g. Role, Permission, Category, Status, Tag)
* **No business lifecycle** — does not move through states like draft → active → closed;
  it is either present or not, or only changes via direct admin edit
* **No independent ownership story** — no single "owner" who creates/updates/uses it the way
  a real business object does

For these entities:
1. Do NOT create a `*-object.md` file for them
2. Do NOT add them to the Object Files index table above
3. In the Relationships table, still record how they relate to real business objects
   (e.g. `User | many-to-one | Role`)
4. Add a short note under the Relationships table pointing to where the entity IS documented —
   typically `docs/specs/data-model.md` (schema), `docs/specs/permissions.md` (if it's
   access-control related), or a relevant `*-process.md` (if there's a management workflow)

Example note:

> **Note on Role:** Role is a configuration entity with no status lifecycle and no
> owner-managed state transitions. It does not have a standalone `role-object.md`.
> Role is documented in `docs/specs/permissions.md` (access control model and seeded
> defaults) and `docs/specs/data-model.md` (schema). The business process for managing
> roles is in `docs/business/role-management-process.md` (if one exists).

If you are unsure whether an entity qualifies for this exception, default to creating
the object file — the exception is for clear cases only, not a shortcut to skip work.

### State Diagram Rules

* Every object file must include a state block if the object has a status lifecycle.
* The state block describes business-level transitions — who triggers them and what the business meaning is.
* Technical state details (ENUM values, DB constraints) belong in docs/specs/data-model.md.
* After writing, run: `python3 docs/script/state_to_html.py docs/business/[object-name]-object.md`

**Canonical source:** The state block in this object file is the single source of truth for state transitions.
`data-model.md` maps ENUM values to these states but must not redefine or contradict transitions.
If transitions differ between the two files, this object file wins — update `data-model.md` to match.

---

## Object Files

| Object | File | Owner |
|---|---|---|
| [e.g., Order] | `docs/business/order-object.md` | [e.g., Customer] |
| [object name] | `docs/business/[object-name]-object.md` | [owner] |

---

## Relationships

| From | Relationship | To | Notes |
|---|---|---|---|
| [Object A] | one-to-many | [Object B] | [e.g., one Order has many OrderItems] |
| [Object A] | many-to-many | [Object C] | via [join object] |

---

## Object File Format

Each object file must follow this format exactly:

```markdown
# [Object Name]

## Description

| Field | Value |
|---|---|
| **Name** | [Object name] |
| **Description** | [What this object represents in the business] |
| **Owner** | [Who owns / is responsible for this object] |
| **Created by** | [Who or what creates it] |
| **Updated by** | [Who or what updates it] |
| **Consumed by** | [Who or what reads / uses it] |

## Status Flow

**Possible statuses:** \`[status1]\`, \`[status2]\`, \`[status3]\`

| From status | To status | Condition | Responsible role |
|---|---|---|---|
| \`[status1]\` | \`[status2]\` | [Business condition, e.g., customer confirms] | [e.g., Customer] |
| \`[status2]\` | \`[status3]\` | [Business condition] | [Role] |

\`\`\`state
title: [Object Name] Lifecycle

[*] -> [status1]
[status1] -> [status2]: [condition] / [responsible role]
[status2] -> [status3]: [condition] / [responsible role]
[status3] -> [*]
\`\`\`

Lifecycle sequence (only if statuses have a fixed order):

\`\`\`
[Status 1]
↓
[Status 2]
↓
[Status 3]
\`\`\`

For each stage:
- Who creates it?
- Who updates it?
- Who uses it?
- Who closes/archives it?
```
