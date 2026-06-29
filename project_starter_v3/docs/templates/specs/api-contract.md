# API Contract

<!--
  Describes the full specification for every API endpoint.
  Each endpoint corresponds to a functional requirement in project-requirements.md.

  Protocol note:
  This template assumes REST over HTTP. If your project uses a different protocol,
  replace the structure of this document to match:

    GraphQL   — document each Query and Mutation: input types, return types, errors
    gRPC      — document each RPC method: request message, response message, error codes
    WebSocket — document each message type: direction (client→server / server→client),
                payload schema, and error handling
    CLI       — document each command: flags, arguments, output format, exit codes

  The sections below (Overview table, per-endpoint blocks, Error Response Format,
  Error Code Catalogue) do not need to be kept if they don't fit your protocol.
  Keep whatever structure best describes how callers interact with your system.
-->

**Base URL:** `[e.g., /api/v1]`
**Authentication:** Bearer Token (JWT)
**Content-Type:** `application/json`

---

## Overview

| Method | Path | Description | Auth |
|---|---|---|---|
| `POST` | `/[resource]` | [description] | ✅ |
| `GET` | `/[resource]` | [description] | ✅ |
| `GET` | `/[resource]/:id` | [description] | ✅ |
| `PATCH` | `/[resource]/:id` | [description] | ✅ |
| `DELETE` | `/[resource]/:id` | [description] | ✅ |

---

## `POST /[resource]`

**Description:** [description]

**Request Body:**

```json
{
  "[field]": "string",   // required
  "[field]": 0,          // required
  "[field]": "string"    // optional
}
```

**Validation Rules:**

| Field | Required | Rule | Error code |
|---|---|---|---|
| `[field]` | ✅ | Length 1–255 | `VALIDATION_FIELD_REQUIRED` |
| `[field]` | ✅ | Range 1–1000 | `VALIDATION_FIELD_OUT_OF_RANGE` |
| `[field]` | ❌ | Format: email | `VALIDATION_FIELD_FORMAT` |

**Success `201 Created`:**

```json
{
  "id": "uuid",
  "[field]": "string",
  "created_at": "2025-01-01T00:00:00Z"
}
```

**Errors:**

| HTTP | Error code | Scenario |
|---|---|---|
| `400` | `VALIDATION_FIELD_REQUIRED` | Required field missing |
| `401` | `AUTH_TOKEN_EXPIRED` | Token expired |
| `409` | `[ENTITY]_ALREADY_EXISTS` | Duplicate resource |

---

## `GET /[resource]`

**Description:** [description]

**Query Parameters:**

| Parameter | Required | Default | Description |
|---|---|---|---|
| `page` | ❌ | `1` | Page number |
| `per_page` | ❌ | `20` | Items per page, max 100 |
| `status` | ❌ | — | Filter by status |

**Success `200 OK`:**

```json
{
  "data": [
    {
      "id": "uuid",
      "[field]": "string",
      "created_at": "2025-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

**Errors:**

| HTTP | Error code | Scenario |
|---|---|---|
| `400` | `VALIDATION_ENUM_INVALID` | Invalid status value |
| `401` | `AUTH_TOKEN_EXPIRED` | Token expired |

---

## `GET /[resource]/:id`

**Description:** [description]

**Success `200 OK`:** Returns the full resource

**Errors:**

| HTTP | Error code | Scenario |
|---|---|---|
| `401` | `AUTH_TOKEN_EXPIRED` | Token expired |
| `403` | `AUTH_RESOURCE_NOT_OWNED` | Accessing another user's resource |
| `404` | `[ENTITY]_NOT_FOUND` | ID does not exist |

---

## `PATCH /[resource]/:id`

**Description:** Partial update — only send fields to change

**Request Body:** Same as POST, but all fields are optional

**Success `200 OK`:** Returns the updated full resource

**Errors:**

| HTTP | Error code | Scenario |
|---|---|---|
| `401` | `AUTH_TOKEN_EXPIRED` | Token expired |
| `403` | `AUTH_RESOURCE_NOT_OWNED` | Modifying another user's resource |
| `404` | `[ENTITY]_NOT_FOUND` | ID does not exist |
| `409` | `[ENTITY]_STATE_INVALID` | Current state does not allow this operation |
| `409` | `[ENTITY]_CONCURRENT_UPDATE` | Optimistic lock conflict |

---

## `DELETE /[resource]/:id`

**Description:** [Soft delete / Hard delete]

**Success `204 No Content`**

**Errors:**

| HTTP | Error code | Scenario |
|---|---|---|
| `401` | `AUTH_TOKEN_EXPIRED` | Token expired |
| `403` | `AUTH_RESOURCE_NOT_OWNED` | Deleting another user's resource |
| `404` | `[ENTITY]_NOT_FOUND` | ID does not exist |
| `409` | `[ENTITY]_STATE_INVALID` | Current state does not allow deletion |

---

## Error Response Format

All errors use a unified format:

```json
{
  "error": {
    "code": "VALIDATION_FIELD_REQUIRED",
    "message": "Field [field] is required",
    "user_message": "[Field name] is required"
  }
}
```

---

## Error Code Catalogue

| Code | HTTP | Description | Retryable |
|---|---|---|---|
| `AUTH_TOKEN_MISSING` | 401 | Authorization header missing | N |
| `AUTH_TOKEN_EXPIRED` | 401 | Token has expired | N |
| `AUTH_TOKEN_INVALID` | 401 | Token verification failed | N |
| `AUTH_PERMISSION_DENIED` | 403 | Role lacks required permission | N |
| `AUTH_RESOURCE_NOT_OWNED` | 403 | Resource does not belong to current user | N |
| `VALIDATION_FIELD_REQUIRED` | 400 | Required field missing | Y |
| `VALIDATION_FIELD_FORMAT` | 400 | Field format invalid | Y |
| `VALIDATION_FIELD_TOO_LONG` | 400 | Field exceeds maximum length | Y |
| `VALIDATION_FIELD_OUT_OF_RANGE` | 400 | Value out of allowed range | Y |
| `VALIDATION_ENUM_INVALID` | 400 | Invalid enum value | Y |
| `[ENTITY]_NOT_FOUND` | 404 | Resource does not exist | N |
| `[ENTITY]_DELETED` | 410 | Resource has been permanently deleted | N |
| `[ENTITY]_ALREADY_EXISTS` | 409 | Resource already exists | N |
| `[ENTITY]_STATE_INVALID` | 409 | Current state does not allow this operation | N |
| `[ENTITY]_CONCURRENT_UPDATE` | 409 | Optimistic lock conflict | Y |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests | Y |
| `EXTERNAL_[SERVICE]_TIMEOUT` | 504 | Upstream service timed out | Y |
| `INTERNAL_UNEXPECTED` | 500 | Unexpected internal error | Y |
