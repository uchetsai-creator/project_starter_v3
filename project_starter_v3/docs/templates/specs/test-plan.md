# Test Plan

<!--
  Describes the testing strategy for this project.
  This file defines WHAT will be tested and HOW.
  Actual test results go in test-report.md.

  Update when:
  - A new module is added (add test scope)
  - Testing tools or CI configuration changes
  - Coverage targets change
-->

---

## Testing Strategy

| Type | Tool | Scope | Coverage target |
|---|---|---|---|
| Unit | [e.g., Jest / pytest / go test] | [e.g., service layer, utility functions] | [e.g., ≥ 80%] |
| Integration | [e.g., Supertest / httpx] | [e.g., API endpoints, DB queries] | [e.g., all endpoints] |
| E2E | [e.g., Playwright / Cypress] | [e.g., critical user flows] | [e.g., happy paths only] |
| Performance | [e.g., k6 / Artillery] | [e.g., peak load scenarios] | [e.g., p95 < 200ms] |

---

## Test Scope

### In Scope

| Module / Feature | Test types | Notes |
|---|---|---|
| [e.g., Auth] | Unit, Integration | [e.g., focus on token validation and expiry] |
| [Module] | [Types] | [Notes] |

### Out of Scope

| Area | Reason |
|---|---|
| [e.g., Third-party payment gateway internals] | [e.g., tested by provider, not our responsibility] |

---

## Test Environment

| Environment | Purpose | Data |
|---|---|---|
| Local | Developer testing | Seed data from `prisma/seed.ts` (or equivalent) |
| CI | Automated tests on every PR | Isolated test DB, reset between runs |
| Staging | Pre-release manual testing | Anonymised production-like data |

---

## CI Integration

```bash
# Run all tests
[e.g., npm test / pytest / go test ./...]

# Run with coverage
[e.g., npm run test:coverage / pytest --cov]

# Run E2E tests
[e.g., npx playwright test]
```

CI must pass before merging to main. Failing tests block deployment.

---

## Test Data Strategy

| Data type | Source | Reset strategy |
|---|---|---|
| Seed data | [e.g., prisma/seed.ts] | [e.g., reset before each test suite] |
| Fixtures | [e.g., tests/fixtures/] | [e.g., static files committed to repo] |
| Mocks | [e.g., MSW / pytest-mock] | [e.g., per-test setup and teardown] |
