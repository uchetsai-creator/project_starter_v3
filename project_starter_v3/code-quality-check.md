# Code Quality Check

Used during the "retrofitting an existing project" flow (see AGENTS.md).
Run this after reading the codebase (Step 1), before writing any documents (Step 2).

---

## Instructions

After reading the entry point, data layer, and one complete vertical slice, produce the report below.
Do not start writing documents until all High severity issues are resolved.

---

## Report Format

**Code Quality Check — [Project Name]**

| Area | Finding | Severity | Recommendation |
|---|---|---|---|
| Layering | [e.g., business logic found in controller] | High / Medium / Low | [what to fix] |
| Package First | [e.g., custom utility duplicates an existing package] | High / Medium / Low | [what to fix] |
| Naming | [e.g., inconsistent module or function naming] | High / Medium / Low | [what to fix] |
| Schema | [e.g., missing indexes for common query patterns] | High / Medium / Low | [what to fix] |
| Security | [e.g., endpoint missing auth check] | High / Medium / Low | [what to fix] |
| Error Handling | [e.g., unhandled promise rejections, missing try/catch] | High / Medium / Low | [what to fix] |
| Permission Consistency | [e.g., role X is responsible for action Y in business process but has no access to the required endpoint] | High / Medium / Low | [grant access or document why a different path is used] |
| State Machine Consistency | [e.g., WorkOrder transitions in business-objects.md and data-model.md conflict — running → cancelled exists in one but not the other] | High / Medium / Low | [align to business-objects.md as canonical source] |
| API Endpoint Overlap | [e.g., PATCH /:id/acknowledge and PATCH /:id/acknowledgement both affect alarm state with no Design Note explaining the split] | Medium / Low | [consolidate or add Design Note with justification] |
| Other | [any other notable issue] | High / Medium / Low | [what to fix] |

If an area has no issues, omit it from the table.

---

## Severity Guide

| Severity | Meaning | Action |
|---|---|---|
| High | Likely to cause bugs, security issues, or maintenance problems | Fix immediately before proceeding to Step 2 |
| Medium | Not urgent but worth fixing before the next feature is added | Add to docs/project-plan.md as a task |
| Low | Minor issue, can be addressed later | Add to docs/project-plan.md as a task |

---

## Area-Specific Notes

**Permission Consistency**
A role that is assigned a business responsibility but denied the required endpoint is always
High severity — it means the business process cannot be executed as documented. Check by:
1. Reading every `*-process.md` and noting each (role, action) pair
2. Cross-referencing against the API Endpoint Access table in `permissions.md`
3. Any gap = High severity finding

**State Machine Consistency**
`business/*-object.md` is the canonical source for state transitions.
`data-model.md` maps ENUM values to those states but must not contradict them.
If transitions differ between the two files, the object file wins — flag the data-model
entry as a High severity finding and align it.

**API Endpoint Overlap**
Two endpoints that affect the same state or resource without a documented reason are
Medium severity. They may not be bugs today, but they create confusion for future
implementers. Check by scanning endpoints with similar paths (e.g., /:id/acknowledge
vs /:id/acknowledgement) and verifying each has a distinct, documented purpose.

---

## After the Report

**High severity issues — fix immediately:**
Fix them one by one before proceeding to Step 2. Follow AGENTS.md principles:
Package First, no unrelated refactor, incremental changes only.
After fixing, note what was changed in a brief summary (one line per fix).

**Medium and Low severity issues — fix at end of current sprint:**
Add each finding as a task at the end of the current sprint in docs/project-plan.md.
Use this format:

```
- [ ] [CODE QUALITY] [Area]: [Recommendation]
```

Example:
```
- [ ] [CODE QUALITY] Schema: Add index on orders.status — frequently queried without index
- [ ] [CODE QUALITY] Naming: Standardise repository method names across modules
```

When the current sprint ends and these tasks are completed:
1. Review all remaining incomplete tasks in docs/project-plan.md.
2. Check whether the changes made affect any upcoming tasks — for example, if a function was
   renamed, or a module's interface changed, any task that references that function or module
   may need to be updated.
3. Update affected tasks before marking the sprint as done and moving to the next one.
