# Code Quality Check

Used during the "retrofitting an existing project" flow (see AGENTS.md).
Run this after reading the codebase (Step 1), before writing any documents (Step 2).

---

## Instructions

After reading the entry point, schema, and one complete module, produce the report below.
Do not start writing documents until the report is acknowledged by the user.

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

| Severity | Meaning |
|---|---|
| High | Likely to cause bugs, security issues, or maintenance problems. Fix before documenting. |
| Medium | Not urgent but worth fixing before the next feature is added. |
| Low | Minor issue. Can be addressed later or noted and left as-is. |

---

## After the Report

Ask the user:

> "Would you like to fix any of these issues before we document the current state?
> - If yes: tell me which ones and we will fix them first, then continue to Step 2.
> - If no: we will document the codebase as-is and record the findings in docs/specs/research.md under a Known Issues section."

**If the user chooses to fix issues first:**
Fix them module by module, following the same principles in AGENTS.md (Package First, no unrelated refactor, incremental changes). Then continue to Step 2.

**If the user skips:**
Add the following section to docs/specs/research.md before filling in any other content:

```markdown
## Known Issues

The following issues were found during the initial code quality check.
They were not fixed at the time of documentation and should be addressed in future tasks.

| Area | Finding | Severity |
|---|---|---|
| [Area] | [Finding] | [Severity] |
```
