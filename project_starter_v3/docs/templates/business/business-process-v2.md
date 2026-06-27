# Business Process

<!--
  Describes high-level business workflows and decision points.
  Focus on WHAT happens from a business perspective — not which service or code handles it.
  Detailed technical cross-module calls belong in docs/modules/[module]/[module]-flow.md.

  This file contains the Activity Diagram:
  - Activity Diagram: business steps, decision points, and branches
  - Sequence Diagram belongs in docs/modules/[module]/[module]-flow.md — not here

  After writing, run:
  python3 docs/script/activity_to_html.py docs/business/business-process.md
-->

---

## Business Goal

[What is the purpose of this business process? 1-3 sentences.]

---

## Process Overview

Focus on:
- Major business stages
- Process sequence
- Process ownership

Do not describe:
- Which service handles each step
- Validation logic
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

## Activity Diagram

<!--
  Describes the business flow — steps and decision points only.
  Do not reference specific services, repositories, or technical implementation.
-->

```activity
title: [Business Process Name]

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
```

---

## Decision Points

| Decision | Decision maker | Input | Possible outcomes |
|---|---|---|---|
| [e.g., Stock available?] | [System] | [Order items] | Yes → Reserve / No → Notify out of stock |
| [Decision] | [Decision maker] | [Input] | [Outcomes] |

---

## Exceptions

| Exception | Cause | Handling method | Responsible role |
|---|---|---|---|
| [e.g., Payment timeout] | [External payment API unreachable] | [Retry 3x, then notify ops] | [System / Ops] |
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
