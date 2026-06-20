# Architecture

<!--
  Describes system component overview and data flow.
  Structured YAML block is used by scripts/architecture_to_html.py to generate the architecture diagram.

  Code layering / module patterns -> docs/architecture/backend.md, docs/architecture/frontend.md
  Database entity relationships (conceptual) -> docs/architecture/database.md
  Deployment environment details -> docs/architecture/deployment.md
-->

## Overview

[Brief description of the system architecture, covering main components and core data flow. 2-4 sentences.]

---

## System Components

| Component | Type | Responsibility | Protocol |
|---|---|---|---|
| [component name] | gateway | [responsibility] | HTTP |
| [component name] | service | [responsibility] | REST |
| [component name] | database | [responsibility] | TCP |
| [component name] | cache | [responsibility] | TCP |
| [component name] | queue | [responsibility] | AMQP |

---

## Data Flow

### Main Path
1. [Component A] → [Component B]: [description]
2. [Component B] → [Component C]: [description]

### Async Path
1. [Component A] → [Queue]: [event sent]
2. [Queue] → [Component B]: [event subscribed]

### Error Path
1. [error scenario] → [how the component handles it]

---

## Structured Definition (for architecture_to_html.py)

```yaml
components:
  - name: [component name]
    type: gateway
    responsibilities:
      - [responsibility 1]
      - [responsibility 2]
    communicates_with:
      - [component name]
    protocol: HTTP

  - name: [component name]
    type: service
    responsibilities:
      - [responsibility 1]
      - [responsibility 2]
    communicates_with:
      - [component name]
    protocol: REST

  - name: [component name]
    type: database
    responsibilities:
      - persistent_storage
    communicates_with: []
    protocol: TCP

  - name: [component name]
    type: cache
    responsibilities:
      - [responsibility]
    communicates_with: []
    protocol: TCP

  - name: [component name]
    type: queue
    responsibilities:
      - async_event_bus
    communicates_with: []
    protocol: AMQP

data_flows:
  - from: [component name]
    to: [component name]
    trigger: [trigger condition]
    protocol: HTTP

  - from: [component name]
    to: [component name]
    trigger: [trigger condition]
    protocol: REST

  - from: [component name]
    to: [component name]
    trigger: [event name]
    protocol: AMQP
```

<!--
  Deployment environment details (services, env vars, startup flow, build/deploy flow)
  belong in docs/architecture/deployment.md — not duplicated here.
-->
