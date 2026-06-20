# Data Model

<!--
  描述資料庫設計。
  對應 business-objects.md 的技術實作層。
-->

## [Entity 名稱] (`[table_name]`)

**用途:** [說明這個資料表存什麼]

| 欄位 | 型別 | 約束 | 說明 |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | 主鍵 |
| `[field]` | VARCHAR(255) | NOT NULL | [說明] |
| `[field]` | TEXT | | [說明，可為空] |
| `[fk_field]_id` | UUID | FK → `[table].id`, NOT NULL | [說明] |
| `status` | ENUM | NOT NULL | 見下方狀態機 |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| `updated_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| `deleted_at` | TIMESTAMPTZ | | Soft delete |

**索引:**

| 索引名 | 欄位 | 用途 |
|---|---|---|
| `idx_[table]_[field]` | `[field]` | [對應哪個查詢] |

**狀態機:**

```
[draft] → [active] → [completed]
              ↓
          [cancelled]
```

| 狀態 | 可轉換到 |
|---|---|
| `draft` | `active`, `cancelled` |
| `active` | `completed`, `cancelled` |
| `completed` | — |
| `cancelled` | — |

---

## [Entity 名稱] (`[table_name]`)

**用途:** [說明]

| 欄位 | 型別 | 約束 | 說明 |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | 主鍵 |
| `[field]` | VARCHAR(255) | NOT NULL | [說明] |
| `[fk_field]_id` | UUID | FK → `[table].id`, NOT NULL | [說明] |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| `updated_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

**索引:**

| 索引名 | 欄位 | 用途 |
|---|---|---|
| `idx_[table]_[fk]_id` | `[fk]_id` | 依外鍵查詢 |

---

## Migration 計畫

| 順序 | 檔案名 | 操作 | 可回滾 |
|---|---|---|---|
| 1 | `[timestamp]_create_[table]` | CREATE TABLE | ✅ |
| 2 | `[timestamp]_create_[table]` | CREATE TABLE | ✅ |
| 3 | `[timestamp]_add_index_[table]` | CREATE INDEX | ✅ |
| 4 | `[timestamp]_modify_[col]_[table]` | ALTER TABLE | ⚠️ 需確認資料 |

---

## Query Patterns

| 查詢 | 條件 | 對應索引 |
|---|---|---|
| [說明，e.g., 列出用戶所有訂單] | `user_id = ?` AND `deleted_at IS NULL` | `idx_orders_user_id` |
| [說明] | `status = ?` | `idx_orders_status` |
