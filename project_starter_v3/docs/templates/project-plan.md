# Project Plan

<!--
  Ordering principles:
  1. Shared foundation first
  2. Each feature as a vertical slice: DB → BE → FE
  3. Each task should be roughly half a day to one day of work

  Task naming convention: [Layer] [Feature Name]
  Layer prefixes: DB / BE / FE / MOD / INF

  Code quality tasks (added by code-quality-check.md) use the prefix [CODE QUALITY]
  and are inserted at the end of the current sprint when found.
-->

---

## Shared Foundation

### Task 1: [Foundation Name]

**Goal:** [What this task achieves]

**Files:**
- Create: `[file path]`
- Modify: `[file path]`
- Read: `[file path]`

- [ ] **Step 1: [Step name]**
  [What to do. Expected result: [description]]

- [ ] **Step 2: [Step name]**
  [What to do. Expected result: [description]]

- [ ] **Step 3: Verify**
  [Verification command, e.g., `curl -s http://localhost:4000/health`]
  Expected: [expected output]

---

## [Feature A]

### Task 2: DB [Feature A] Schema

**Goal:** [Description]

**Files:**
- Create: `[migration file path]`

- [ ] **Step 1: [Step name]**
  [Description. Expected result: [description]]

- [ ] **Step 2: Verify**
  [Verification method]
  Expected: [expected result]

---

### Task 3: BE [Feature A]

**Goal:** [Description]

**Files:**
- Create: `[file path]`
- Modify: `[file path]`

- [ ] **Step 1: [Step name]**
  [Description. Expected result: [description]]

- [ ] **Step 2: Verify**
  [Verification command]
  Expected: [expected result]

---

### Task 4: FE [Feature A]

**Goal:** [Description]

**Files:**
- Create: `[file path]`

- [ ] **Step 1: [Step name]**
  [Description]

- [ ] **Step 2: Verify**
  [Verification method]
  Expected: [expected result]

<!--
  [CODE QUALITY] tasks are inserted here, at the end of the current sprint,
  when Medium or Low severity issues are found during code-quality-check.md.

  Format:
  ### Task N: [CODE QUALITY] [Area]: [Recommendation]
  **Goal:** [What to fix and why]
  **Files:**
  - Modify: `[file path]`
  - [ ] **Step 1: [Fix description]**
  - [ ] **Step 2: Verify**
    Expected: [no regressions, behaviour unchanged]

  After completing [CODE QUALITY] tasks, review all remaining incomplete tasks below
  and update any that reference changed function names, module interfaces, or file paths.
-->

---

## [Feature B]

### Task 5: DB [Feature B] Schema

**Goal:** [Description]

**Files:**
- Create: `[file path]`

- [ ] **Step 1: [Step name]**
  [Description]

- [ ] **Step 2: Verify**
  Expected: [expected result]

---

### Task 6: BE [Feature B]

**Goal:** [Description]

**Files:**
- Create: `[file path]`

- [ ] **Step 1: [Step name]**
  [Description]

- [ ] **Step 2: Verify**
  Expected: [expected result]

---

### Task 7: FE [Feature B]

**Goal:** [Description]

**Files:**
- Create: `[file path]`

- [ ] **Step 1: [Step name]**
  [Description]

- [ ] **Step 2: Verify**
  Expected: [expected result]

---

## Completed

* [Task name] — [completion date]
