# Permissions

<!--
  Describes roles, permission definitions, and access control for every API endpoint.
  Corresponds to every endpoint in api-contract.md.
  After writing, run: python3 docs/script/usecase_to_html.py docs/specs/permissions.md
-->

**Access Control Model:** RBAC

---

## Role Definitions

| Role | Description | Inherits from |
|---|---|---|
| `ROLE_GUEST` | Unauthenticated user, public resources only | — |
| `ROLE_USER` | Authenticated user, own resources only | `ROLE_GUEST` |
| `ROLE_ADMIN` | Full access to all resources | `ROLE_USER` |
| `[ROLE_ID]` | [Description] | [Inherits from] |

---

## Permission Definitions

| Permission | Description |
|---|---|
| `[resource]:read` | Read [resource] |
| `[resource]:create` | Create [resource] |
| `[resource]:update` | Update own [resource] |
| `[resource]:update:any` | Update any [resource] |
| `[resource]:delete` | Delete own [resource] |
| `[resource]:delete:any` | Delete any [resource] |

---

## RBAC Matrix

<!--
  ✅ Allowed
  ❌ Denied
  🔶 Conditionally allowed (see notes below)
-->

| Permission | ROLE_GUEST | ROLE_USER | ROLE_ADMIN |
|---|---|---|---|
| `[resource]:read` | ✅ | ✅ | ✅ |
| `[resource]:create` | ❌ | ✅ | ✅ |
| `[resource]:update` | ❌ | 🔶 | ✅ |
| `[resource]:update:any` | ❌ | ❌ | ✅ |
| `[resource]:delete` | ❌ | 🔶 | ✅ |
| `[resource]:delete:any` | ❌ | ❌ | ✅ |

**🔶 Conditions:**
* `[resource]:update` — `ROLE_USER` may only update resources where `owner_id = current_user.id`
* `[resource]:delete` — `ROLE_USER` may only delete resources where `owner_id = current_user.id`

---

## API Endpoint Access

| Method | Path | Required permission | Minimum role | Extra condition |
|---|---|---|---|---|
| `POST` | `/[resource]` | `[resource]:create` | `ROLE_USER` | — |
| `GET` | `/[resource]` | `[resource]:read` | `ROLE_GUEST` | — |
| `GET` | `/[resource]/:id` | `[resource]:read` | `ROLE_GUEST` | — |
| `PATCH` | `/[resource]/:id` | `[resource]:update` | `ROLE_USER` | Own resource only |
| `DELETE` | `/[resource]/:id` | `[resource]:delete` | `ROLE_USER` | Own resource only |

---

## Enforcement Layers

| Layer | Responsibility |
|---|---|
| API Gateway | JWT validation, role extraction |
| Middleware | Role-permission check, reject unauthorized (403) |
| Service Layer | Ownership check — `owner_id = current_user.id` |

---

## Edge Cases

| Edge Case | Design | Response |
|---|---|---|
| Unauthenticated access to protected resource | API Gateway JWT check fails | `401 AUTH_TOKEN_MISSING` |
| Low-privilege role attempts high-privilege action | Middleware role check | `403 AUTH_PERMISSION_DENIED` |
| User accesses another user's resource | Service Layer ownership check | `403 AUTH_RESOURCE_NOT_OWNED` |
| Expired token | API Gateway JWT check fails | `401 AUTH_TOKEN_EXPIRED` |

---

## Use Case Diagram

<!--
  System-level view — list ALL roles and ALL major functions across all modules.
  Not per resource, not per module — the whole system in one diagram.
  After writing, run: python3 docs/script/usecase_to_html.py docs/specs/permissions.md
-->

```usecase
title: [System Name] — Access Control

actor Guest
actor User
actor Admin

# [Feature A]
usecase "[Feature A] Read" as UC1
usecase "[Feature A] Create" as UC2
usecase "[Feature A] Update Own" as UC3
usecase "[Feature A] Delete Own" as UC4
usecase "[Feature A] Manage All" as UC5

# [Feature B]
usecase "[Feature B] Read" as UC6
usecase "[Feature B] Create" as UC7
usecase "[Feature B] Manage All" as UC8

# [Admin only]
usecase "[Admin Feature] Configure" as UC9

Guest --> UC1
User --> UC1
User --> UC2
User --> UC3
User --> UC4
User --> UC6
User --> UC7
Admin --> UC1
Admin --> UC2
Admin --> UC3
Admin --> UC4
Admin --> UC5
Admin --> UC6
Admin --> UC7
Admin --> UC8
Admin --> UC9
```
