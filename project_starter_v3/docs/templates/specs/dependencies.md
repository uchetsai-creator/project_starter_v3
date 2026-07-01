# Dependencies

<!--
  Lists every external dependency the system relies on.
  Update when a package is added, removed, or its version is pinned or changed.

  Sections:
    Runtime Dependencies   — packages needed to run the application in production
    Dev Dependencies       — packages needed only for development, testing, or build
    External Services      — third-party APIs, cloud services, SaaS tools
    Infrastructure         — databases, message queues, caches, storage

  For Runtime and Dev Dependencies, list the actual package manager entries.
  For External Services, document the integration point and fallback behaviour.
-->

---

## Runtime Dependencies

<!--
  List the packages and their pinned versions used in production.
  Group by layer (Backend / Frontend / Mobile) if the project has multiple.

  For Node.js projects: mirror key entries from package.json dependencies
  For Python projects: mirror requirements.txt or pyproject.toml
  For Go: mirror go.mod require block
  For other ecosystems: use the equivalent package manifest format
-->

| Package | Version | Purpose |
|---|---|---|
| [package-name] | [e.g., ^4.18.2] | [What it does in this project] |

---

## Dev Dependencies

| Package | Version | Purpose |
|---|---|---|
| [package-name] | [version] | [e.g., unit testing, linting, bundling] |

---

## External Services

<!--
  List every third-party API, SaaS, or managed cloud service the system calls.
  Document the integration point (which module calls it) and what happens if it is unavailable.
-->

| Service | Provider | Used by | Fallback behaviour |
|---|---|---|---|
| [e.g., Email delivery] | [e.g., SendGrid] | [e.g., notification module] | [e.g., retry 3x, then dead-letter queue] |
| [Service name] | [Provider] | [Module] | [Fallback] |

---

## Infrastructure

<!--
  List the infrastructure components the application depends on at runtime.
  These are not packages — they are services that must be running.
  Cross-reference with docs/architecture/deployment.md for startup and configuration details.
-->

| Component | Technology | Version | Purpose |
|---|---|---|---|
| [e.g., Primary database] | [e.g., PostgreSQL] | [e.g., 16] | [persistent storage] |
| [e.g., Cache] | [e.g., Redis] | [e.g., 7] | [session storage, query cache] |
| [Component] | [Technology] | [Version] | [Purpose] |
