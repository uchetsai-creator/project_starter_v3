# Business Process

Understand the business before understanding the system.

---

## Business Goal

[What is the purpose of this business process? 1-3 sentences.]

---

## Process Overview

Describe high-level business workflows.

Focus on:
- Major business stages
- Process sequence
- Process ownership

Do not describe:
- Detailed execution steps
- Validation logic
- System behavior
- Database actions

```
Start → [Stage 1] → [Stage 2] → [Stage 3] → End
```

---

## Process Steps

| Step | Owner | Input | Action | Output | Next step |
|---|---|---|---|---|---|
| [Step name] | [Owner] | [Input] | [What happens] | [Output] | [Next step] |
| [Step name] | [Owner] | [Input] | [What happens] | [Output] | [Next step] |

---

## Decision Points

| Decision | Decision maker | Input | Possible outcomes |
|---|---|---|---|
| [e.g., Approve order?] | [Manager] | [Order amount, history] | Approved → next step / Rejected → notify user |

For decisions with multiple branches or non-trivial logic, use a diagram instead:

```
Trigger
↓
Validation
↓
Decision?
├─ Yes → Action A
└─ No  → Action B
```

---

## Exceptions

| Exception | Cause | Handling method | Responsible role |
|---|---|---|---|
| [e.g., Payment timeout] | [External payment API unreachable] | [Retry 3x, then notify ops team] | [System / Ops] |
| [Exception] | [Cause] | [How it is handled] | [Who handles it] |

---

## Pain Points

| Current problem | Impact | Current workaround |
|---|---|---|
| [Problem] | [Impact on business] | [What people do today] |

---

## Future Improvement Ideas

| Improvement | Expected benefit |
|---|---|
| [Idea] | [What it would improve] |
