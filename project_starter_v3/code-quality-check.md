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
