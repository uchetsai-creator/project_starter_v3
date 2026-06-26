# module-flow.md

Purpose:

Describe detailed execution steps for a business process.

Create a dedicated flow document when a business process requires operational detail.

Rules:

- Focus on execution flow
- Include business actions
- Include system actions when relevant
- Keep chronological order
- One flow document per business process
- Include all three formats below: text (quick read), activity block (execution steps), sequence block (cross-service calls)
- After writing, run:
  - python3 docs/script/activity_to_html.py <this-file>
  - python3 docs/script/sequence_to_html.py <this-file>

---

## Process: [Flow Name]

### Text Overview

```
[Step A]
↓
[Step B]
↓
[Decision Point]?
├─ Yes → [Step C]
└─ No  → [Step D]
↓
[Step E]
```

### Activity Diagram

```activity
title: [Flow Name]

start
:[Step A];
:[Step B];
if ([Decision Point]?) then (yes)
  :[Step C];
else (no)
  :[Step D];
endif
:[Step E];
stop
```

### Sequence Diagram

```sequence
title: [Flow Name]

[Service A] -> [Service B]: [message / action]
[Service B] -> [Service C]: [message / action]
[Service C] --> [Service B]: [response]
[Service B] --> [Service A]: [response]
```
