# [Module Name] Flow

<!--
  Describes cross-module interactions for a specific business process.
  One flow file per process (e.g., order-flow.md, payment-flow.md).

  This file contains the Sequence Diagram only:
  - Sequence Diagram: which service calls which service, in what order
  - Activity Diagram belongs in docs/business/business-process.md — not here

  After writing, run:
  python3 docs/script/sequence_to_html.py docs/modules/[module]/[module]-flow.md

  Naming convention: [module-name]-flow.md
  Location: docs/modules/[module]/[module]-flow.md
  Example: docs/modules/order/order-flow.md
-->

---

## Process: [Flow Name, e.g., Create Order]

### Text Overview

Cross-module call sequence at a glance:

```
[Caller] → [Service A]: [action]
           [Service A] → [Service B]: [action]
                         [Service B] → [Service C]: [action]
                         [Service C] → [Service B]: [response]
           [Service A] ← [Service B]: [response]
[Caller] ← [Service A]: [final response]
```

### Sequence Diagram

```sequence
title: [Flow Name]

[Client / Entry Point] -> [Service A]: [method or HTTP call]
[Service A] -> [Service B]: [method call]
[Service B] --> [Service A]: [response]
[Service A] -> [Service C]: [method call]
[Service C] --> [Service A]: [response]
[Service A] --> [Client / Entry Point]: [final response]
```

---

## Process: [Another Flow Name, e.g., Cancel Order]

### Text Overview

```
[Caller] → [Service A]: [action]
           [Service A] → [Service B]: [action]
           [Service A] → [Service C]: [action]
[Caller] ← [Service A]: [response]
```

### Sequence Diagram

```sequence
title: [Another Flow Name]

[Client / Entry Point] -> [Service A]: [method or HTTP call]
[Service A] -> [Service B]: [method call]
[Service B] --> [Service A]: [response]
[Service A] -> [Service C]: [method call]
[Service C] --> [Service A]: [response]
[Service A] --> [Client / Entry Point]: [final response]
```
