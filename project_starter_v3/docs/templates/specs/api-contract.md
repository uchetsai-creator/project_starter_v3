# API Contract

<!--
  描述所有 API endpoint 的完整規格。
  每個 endpoint 對應 project-requirements.md 的 FR。
-->

**Base URL:** `[e.g., /api/v1]`
**認證:** Bearer Token (JWT)
**Content-Type:** `application/json`

---

## 總覽

| Method | Path | 說明 | 認證 |
|---|---|---|---|
| `POST` | `/[resource]` | [說明] | ✅ |
| `GET` | `/[resource]` | [說明] | ✅ |
| `GET` | `/[resource]/:id` | [說明] | ✅ |
| `PATCH` | `/[resource]/:id` | [說明] | ✅ |
| `DELETE` | `/[resource]/:id` | [說明] | ✅ |

---

## `POST /[resource]`

**說明:** [說明]

**Request Body:**

```json
{
  "[field]": "string",   // 必填
  "[field]": 0,          // 必填
  "[field]": "string"    // 選填
}
```

**驗證規則:**

| 欄位 | 必填 | 規則 | 錯誤碼 |
|---|---|---|---|
| `[field]` | ✅ | 長度 1–255 | `VALIDATION_FIELD_REQUIRED` |
| `[field]` | ✅ | 範圍 1–1000 | `VALIDATION_FIELD_OUT_OF_RANGE` |
| `[field]` | ❌ | 格式：email | `VALIDATION_FIELD_FORMAT` |

**成功 `201 Created`:**

```json
{
  "id": "uuid",
  "[field]": "string",
  "created_at": "2025-01-01T00:00:00Z"
}
```

**錯誤:**

| HTTP | 錯誤碼 | 情境 |
|---|---|---|
| `400` | `VALIDATION_FIELD_REQUIRED` | 必填欄位缺失 |
| `401` | `AUTH_TOKEN_EXPIRED` | Token 過期 |
| `409` | `[ENTITY]_ALREADY_EXISTS` | 重複建立 |

---

## `GET /[resource]`

**說明:** [說明]

**Query Parameters:**

| 參數 | 必填 | 預設值 | 說明 |
|---|---|---|---|
| `page` | ❌ | `1` | 頁碼 |
| `per_page` | ❌ | `20` | 每頁筆數，最大 100 |
| `status` | ❌ | — | 過濾狀態 |

**成功 `200 OK`:**

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

**錯誤:**

| HTTP | 錯誤碼 | 情境 |
|---|---|---|
| `400` | `VALIDATION_ENUM_INVALID` | status 傳入不合法的值 |
| `401` | `AUTH_TOKEN_EXPIRED` | Token 過期 |

---

## `GET /[resource]/:id`

**說明:** [說明]

**成功 `200 OK`:** 回傳單一資源完整欄位

**錯誤:**

| HTTP | 錯誤碼 | 情境 |
|---|---|---|
| `401` | `AUTH_TOKEN_EXPIRED` | Token 過期 |
| `403` | `AUTH_RESOURCE_NOT_OWNED` | 存取不屬於自己的資源 |
| `404` | `[ENTITY]_NOT_FOUND` | ID 不存在 |

---

## `PATCH /[resource]/:id`

**說明:** 部分更新，只傳要修改的欄位

**Request Body:** 同 POST，但所有欄位改為選填

**成功 `200 OK`:** 回傳更新後的完整資源

**錯誤:**

| HTTP | 錯誤碼 | 情境 |
|---|---|---|
| `401` | `AUTH_TOKEN_EXPIRED` | Token 過期 |
| `403` | `AUTH_RESOURCE_NOT_OWNED` | 修改不屬於自己的資源 |
| `404` | `[ENTITY]_NOT_FOUND` | ID 不存在 |
| `409` | `[ENTITY]_STATE_INVALID` | 當前狀態不允許此操作 |
| `409` | `[ENTITY]_CONCURRENT_UPDATE` | 樂觀鎖衝突 |

---

## `DELETE /[resource]/:id`

**說明:** [Soft delete / Hard delete]

**成功 `204 No Content`**

**錯誤:**

| HTTP | 錯誤碼 | 情境 |
|---|---|---|
| `401` | `AUTH_TOKEN_EXPIRED` | Token 過期 |
| `403` | `AUTH_RESOURCE_NOT_OWNED` | 刪除不屬於自己的資源 |
| `404` | `[ENTITY]_NOT_FOUND` | ID 不存在 |
| `409` | `[ENTITY]_STATE_INVALID` | 當前狀態不允許刪除 |

---

## 錯誤回應格式

所有錯誤統一格式：

```json
{
  "error": {
    "code": "VALIDATION_FIELD_REQUIRED",
    "message": "Field [field] is required",
    "user_message": "[欄位名稱] 為必填"
  }
}
```

---

## Error Code Catalogue

| Code | HTTP | 說明 | Retryable |
|---|---|---|---|
| `AUTH_TOKEN_MISSING` | 401 | Authorization header 缺失 | N |
| `AUTH_TOKEN_EXPIRED` | 401 | Token 已過期 | N |
| `AUTH_TOKEN_INVALID` | 401 | Token 驗證失敗 | N |
| `AUTH_PERMISSION_DENIED` | 403 | 角色無此權限 | N |
| `AUTH_RESOURCE_NOT_OWNED` | 403 | 資源不屬於當前用戶 | N |
| `VALIDATION_FIELD_REQUIRED` | 400 | 必填欄位缺失 | Y |
| `VALIDATION_FIELD_FORMAT` | 400 | 欄位格式錯誤 | Y |
| `VALIDATION_FIELD_TOO_LONG` | 400 | 欄位超過最大長度 | Y |
| `VALIDATION_FIELD_OUT_OF_RANGE` | 400 | 數值超出範圍 | Y |
| `VALIDATION_ENUM_INVALID` | 400 | 非法的 enum 值 | Y |
| `[ENTITY]_NOT_FOUND` | 404 | 資源不存在 | N |
| `[ENTITY]_DELETED` | 410 | 資源已被刪除 | N |
| `[ENTITY]_ALREADY_EXISTS` | 409 | 資源已存在 | N |
| `[ENTITY]_STATE_INVALID` | 409 | 當前狀態不允許此操作 | N |
| `[ENTITY]_CONCURRENT_UPDATE` | 409 | 樂觀鎖衝突 | Y |
| `RATE_LIMIT_EXCEEDED` | 429 | 請求過於頻繁 | Y |
| `EXTERNAL_[SERVICE]_TIMEOUT` | 504 | 外部服務逾時 | Y |
| `INTERNAL_UNEXPECTED` | 500 | 系統內部錯誤 | Y |
