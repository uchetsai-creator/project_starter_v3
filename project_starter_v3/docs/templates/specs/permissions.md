# Permissions

<!--
  描述角色、權限定義、以及每個 API endpoint 的存取控制。
  對應 api-contract.md 的每個 endpoint。
-->

**存取控制模型:** RBAC

---

## 角色定義

| 角色 | 說明 | 繼承自 |
|---|---|---|
| `ROLE_GUEST` | 未登入用戶，只能存取公開資源 | — |
| `ROLE_USER` | 已登入用戶，只能操作自己的資源 | `ROLE_GUEST` |
| `ROLE_ADMIN` | 可操作所有用戶的資源 | `ROLE_USER` |
| `[ROLE_ID]` | [說明] | [繼承自] |

---

## 權限定義

| 權限 | 說明 |
|---|---|
| `[resource]:read` | 讀取 [資源] |
| `[resource]:create` | 建立 [資源] |
| `[resource]:update` | 更新自己的 [資源] |
| `[resource]:update:any` | 更新任何人的 [資源] |
| `[resource]:delete` | 刪除自己的 [資源] |
| `[resource]:delete:any` | 刪除任何人的 [資源] |

---

## 角色權限矩陣

<!--
  ✅ 允許
  ❌ 拒絕
  🔶 條件允許（見下方說明）
-->

| 權限 | ROLE_GUEST | ROLE_USER | ROLE_ADMIN |
|---|---|---|---|
| `[resource]:read` | ✅ | ✅ | ✅ |
| `[resource]:create` | ❌ | ✅ | ✅ |
| `[resource]:update` | ❌ | 🔶 | ✅ |
| `[resource]:update:any` | ❌ | ❌ | ✅ |
| `[resource]:delete` | ❌ | 🔶 | ✅ |
| `[resource]:delete:any` | ❌ | ❌ | ✅ |

**🔶 條件說明:**
* `[resource]:update` — `ROLE_USER` 只能更新 `owner_id = current_user.id` 的資源
* `[resource]:delete` — `ROLE_USER` 只能刪除 `owner_id = current_user.id` 的資源

---

## API Endpoint 權限對應

| Method | Path | 所需權限 | 最低角色 | 額外條件 |
|---|---|---|---|---|
| `POST` | `/[resource]` | `[resource]:create` | `ROLE_USER` | — |
| `GET` | `/[resource]` | `[resource]:read` | `ROLE_GUEST` | — |
| `GET` | `/[resource]/:id` | `[resource]:read` | `ROLE_GUEST` | — |
| `PATCH` | `/[resource]/:id` | `[resource]:update` | `ROLE_USER` | 僅限 `owner_id = current_user.id` |
| `DELETE` | `/[resource]/:id` | `[resource]:delete` | `ROLE_USER` | 僅限 `owner_id = current_user.id` |

---

## 權限執行層

| 層級 | 負責什麼 |
|---|---|
| API Gateway | JWT 驗證、角色解析 |
| Middleware | 角色權限檢查，拒絕無權限請求（403） |
| Service Layer | 所有權檢查，確認 `owner_id = current_user.id` |

---

## 對應 Edge Cases

| Edge Case | 對應設計 | 回應 |
|---|---|---|
| 未認證用戶存取受保護資源 | API Gateway JWT 驗證失敗 | `401 AUTH_TOKEN_MISSING` |
| 低權限角色執行高權限操作 | Middleware 角色檢查 | `403 AUTH_PERMISSION_DENIED` |
| 用戶存取不屬於自己的資源 | Service Layer 所有權檢查 | `403 AUTH_RESOURCE_NOT_OWNED` |
| Token 已過期 | API Gateway JWT 驗證失敗 | `401 AUTH_TOKEN_EXPIRED` |
