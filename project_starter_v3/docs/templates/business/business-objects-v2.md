# Business Objects

Identify the important business entities, their relationships, and lifecycle.

---

## [Object Name]

| Field | Value |
|---|---|
| **Name** | [Object name] |
| **Description** | [What this object represents in the business] |
| **Owner** | [Who owns / is responsible for this object] |
| **Created by** | [Who or what creates it] |
| **Updated by** | [Who or what updates it] |
| **Consumed by** | [Who or what reads / uses it] |

---

## [Object Name]

| Field | Value |
|---|---|
| **Name** | [Object name] |
| **Description** | [What this object represents] |
| **Owner** | [Owner] |
| **Created by** | [Creator] |
| **Updated by** | [Updater] |
| **Consumed by** | [Consumer] |

---

## Relationships

| From | Relationship | To | Notes |
|---|---|---|---|
| [Object A] | one-to-many | [Object B] | [e.g., one Order has many OrderItems] |
| [Object A] | many-to-many | [Object C] | via [join object] |

---

## Status Flow

### [Object Name]

**Possible statuses:** `[status1]`, `[status2]`, `[status3]`

| From status | To status | Condition | Responsible role |
|---|---|---|---|
| `[status1]` | `[status2]` | [Condition] | [Role] |
| `[status2]` | `[status3]` | [Condition] | [Role] |
| `[status2]` | `[status1]` | [Condition] | [Role] |

Lifecycle sequence (only if statuses have a fixed order):

```
[Status 1]
↓
[Status 2]
↓
[Status 3]
```

For each stage:
- Who creates it?
- Who updates it?
- Who uses it?
- Who closes/archives it?
