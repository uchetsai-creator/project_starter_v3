# Business Process Index

<!--
  This file is the index and rule definition for all business process documents.
  Each business process has its own dedicated file under docs/business/.
  Each process file must follow the rules and format defined in this document.

  Naming convention: [process-name]-process.md
  Location: docs/business/[process-name]-process.md
  Examples:
    docs/business/order-create-process.md
    docs/business/order-cancel-process.md
    docs/business/inventory-restock-process.md

  Files matching *-process.md are automatically included in the PDF.
  After writing a new process file, run:
  python3 docs/script/activity_to_html.py docs/business/[process-name]-process.md
-->

---

## Rules

* This file acts as the index and rule definition.
* Do not put process content in this file.
* Each business process must have its own file.
* Each process file must follow the rules and format defined in this document.

### Content Rules

* Focus on WHAT happens from a business perspective.
* Do not describe which service or code handles each step.
* Do not describe validation logic or database actions.
* Technical cross-module calls belong in docs/modules/[module]/[module]-flow.md — not here.

### Activity Diagram Rules

* Every process file must include an activity block.
* The activity block describes business steps and decision branches only.
* Do not reference specific services, repositories, or technical implementation in the diagram.
* After writing, run: `python3 docs/script/activity_to_html.py docs/business/[process-name]-process.md`

---

## Process Files

| Process | File | Owner |
|---|---|---|
| [e.g., Create Order] | `docs/business/order-create-process.md` | [e.g., Customer] |
| [process name] | `docs/business/[process-name]-process.md` | [owner] |

---

## Process File Format

Each process file must follow this format exactly:

```markdown
# [Process Name]

## Business Goal
[What is the purpose of this business process? 1-3 sentences.]

## Process Overview

Focus on:
- Major business stages
- Process sequence
- Process ownership

Do not describe:
- Which service handles each step
- Validation logic
- Database actions

\`\`\`
Start → [Stage 1] → [Stage 2] → [Stage 3] → End
\`\`\`

## Process Steps

| Step | Owner | Input | Action | Output | Next step |
|---|---|---|---|---|---|
| [Step name] | [Owner] | [Input] | [What happens] | [Output] | [Next step] |

## Activity Diagram

\`\`\`activity
title: [Process Name]

start
:[Step 1];
:[Step 2];
if ([Decision Point]?) then (yes)
  :[Step 3a];
  if ([Another Decision]?) then (yes)
    :[Step 4a];
  else (no)
    :[Step 4b];
  endif
else (no)
  :[Step 3b];
endif
:[Final Step];
stop
\`\`\`

## Decision Points

| Decision | Decision maker | Input | Possible outcomes |
|---|---|---|---|
| [e.g., Stock available?] | [System] | [Order items] | Yes → Reserve / No → Notify out of stock |

## Exceptions

| Exception | Cause | Handling method | Responsible role |
|---|---|---|---|
| [e.g., Payment timeout] | [External API unreachable] | [Retry 3x, then notify ops] | [System / Ops] |

## Pain Points

| Current problem | Impact | Current workaround |
|---|---|---|
| [Problem] | [Impact on business] | [What people do today] |

## Future Improvement Ideas

| Improvement | Expected benefit |
|---|---|
| [Idea] | [What it would improve] |
```
