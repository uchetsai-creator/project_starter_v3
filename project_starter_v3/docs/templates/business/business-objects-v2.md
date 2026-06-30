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
