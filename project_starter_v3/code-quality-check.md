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

**Medium and Low severity issues — add to project-plan:**
For each Medium/Low finding, add a task to docs/project-plan.md under a
`## Code Quality` sprint/section. Use this format:

```
- [ ] [Area]: [Finding] — [Recommendation]
```

Example:
```
- [ ] Schema: Add index on orders.status — frequently queried without index
- [ ] Naming: Standardise repository method names across modules
```

Do not mention these issues again after adding them to the plan.
They will be handled as normal tasks during development.
