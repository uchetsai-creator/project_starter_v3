# Business Rules

Record business knowledge — constraints, policies, and rules that the system must enforce.

---

## Rules

### BR-001: [Rule Name]

| Field | Value |
|---|---|
| **Rule ID** | BR-001 |
| **Description** | [What the rule enforces] |
| **Reason** | [Why this rule exists] |
| **Owner** | [System / Role / Team] |
| **Impact** | [What happens when the rule is violated] |

### BR-002: [Rule Name]

| Field | Value |
|---|---|
| **Rule ID** | BR-002 |
| **Description** | [What the rule enforces] |
| **Reason** | [Why this rule exists] |
| **Owner** | [System / Role / Team] |
| **Impact** | [What happens when the rule is violated] |

---

## Approval Rules

| Action | Required approver | API / Trigger | Rejection response |
|---|---|---|---|
| [e.g., Role mutation] | Admin role | `POST /api/roles` | 403 for non-admin callers |
| [Action] | [Approver] | [API] | [Response] |

---

## Validation Rules

| Rule | Condition checked | Failure behavior |
|---|---|---|
| [e.g., Report date range] | `from ≤ to` | 400 before DB query |
| [Rule] | [Condition] | [Failure behavior] |

---

## Notification Rules

| When | Who receives | Method |
|---|---|---|
| [e.g., Alarm fires] | [e.g., Users in AlarmRuleRecipient] | [e.g., Push notification] |
| [Trigger] | [Recipient] | [Method] |

---

## Audit Rules

| Action | What is retained |
|---|---|
| [e.g., Alarm acknowledgement] | [e.g., acknowledgedBy, acknowledgedAt] |
| [Action] | [Retained data] |
