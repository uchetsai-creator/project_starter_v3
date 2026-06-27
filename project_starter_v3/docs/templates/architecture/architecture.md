# Architecture

<!--
  Describes system component overview and data flow.
  Structured YAML block is used by scripts/architecture_to_html.py to generate the architecture diagram.

  Code layering / module patterns -> backend.md, frontend.md (same folder)
  Database entity relationships (conceptual) -> database.md (same folder)
  Deployment environment details -> deployment.md (same folder)
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
  belong in deployment.md (same folder) — not duplicated here.
-->

## System Component Structure

<!--
  Describes the code-level component structure of the whole system.
  Frontend, Backend, and Database layers in one diagram.

  Fill in this block based on the actual layers described in:
  - docs/architecture/frontend.md  → replace [Frontend groups and components]
  - docs/architecture/backend.md   → replace [Backend groups and components]
  - docs/architecture/database.md  → replace [Database]

  Use the actual layer names from those documents, not generic placeholders.
  e.g. if backend.md says "Controller → Service → Repository", use those names here.
       if frontend.md says "Page → Hook → API Client", use those names here.

  After writing, run: python3 docs/script/component_to_html.py docs/architecture/architecture.md
-->

```component
title: System Component Structure

group "System" {
  group "Frontend" {
    component "[e.g., Page Layer — from frontend.md]" as FE1 {
      provides: [e.g., UI views, forms]
      requires: FE2
    }
    component "[e.g., Data Layer — from frontend.md]" as FE2 {
      provides: [e.g., API calls, state management]
      requires: Backend Entry
    }
  }
  group "Backend" {
    component "[e.g., Controller — from backend.md]" as BE1 {
      provides: [e.g., HTTP endpoints]
      requires: BE2
    }
    component "[e.g., Service — from backend.md]" as BE2 {
      provides: [e.g., business logic]
      requires: BE3
    }
    component "[e.g., Repository — from backend.md]" as BE3 {
      provides: [e.g., DB queries]
      requires: DB
    }
  }
  component "[e.g., PostgreSQL]" as DB {
    provides: persistent storage
    requires:
  }
}

FE1 --> BE1 : HTTP/REST
FE2 --> BE1 : HTTP/REST
BE1 --> BE2 : uses
BE2 --> BE3 : uses
BE3 --> DB : [e.g., TCP]
```
