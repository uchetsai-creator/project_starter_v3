# Business Rules

Record business knowledge — constraints, policies, and rules that the system must enforce.

<!--
  Enforcement Layer is mandatory for every rule. A rule that only says "operator cannot
  access X" without specifying WHERE it is enforced creates ambiguity: is it a frontend
  page guard only, or does the backend API also block it? If only the frontend enforces
  it, the backend may be unintentionally open. State the layer explicitly so this gap
  cannot occur silently.

  Valid values: Frontend page guard / Backend middleware / Service layer /
                Database constraint / All layers (specify which combination)

  Before writing a rule here, confirm it is a Hardcoded constraint, not a Seeded default:
    - Hardcoded: enforced in code, cannot change without a deployment — belongs here as
      a permanent rule.
    - Seeded default: a starting value in the database (e.g. default role permissions)
      that an admin can change at runtime via a Role Management feature — does NOT
      belong here as a permanent rule. Document it in permissions.md as "(Default)"
      instead.
  Writing a seeded default as a hardcoded rule means this file goes stale the moment
  an admin changes the setting, with nothing to flag the contradiction.
-->

---

## Rules

### BR-001: [Rule Name]

| Field | Value |
|---|---|
| **Rule ID** | BR-001 |
| **Description** | [What the rule enforces] |
| **Reason** | [Why this rule exists] |
| **Owner** | [System / Role / Team] |
| **Enforcement Layer** | [Frontend page guard / Backend middleware / Service layer / Database constraint / All layers] |
| **Impact** | [What happens when the rule is violated] |

### BR-002: [Rule Name]

| Field | Value |
|---|---|
| **Rule ID** | BR-002 |
| **Description** | [What the rule enforces] |
| **Reason** | [Why this rule exists] |
| **Owner** | [System / Role / Team] |
| **Enforcement Layer** | [Frontend page guard / Backend middleware / Service layer / Database constraint / All layers] |
| **Impact** | [What happens when the rule is violated] |

---

## Approval Rules

<!--
  API / Trigger column: describe whatever entry point enforces this rule.
  e.g. HTTP endpoint, CLI command, queue message type, UI action, cron job.
-->

| Action | Required approver | Trigger | Rejection response |
|---|---|---|---|
| [e.g., Role change] | Admin | [e.g., POST /api/roles / admin CLI command] | [e.g., 403 / error message] |
| [Action] | [Approver] | [Trigger] | [Response] |

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
