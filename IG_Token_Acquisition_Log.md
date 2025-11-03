# Instagram Access Token 獲取與除錯紀錄 (2025/11/03)

## 總結
本次任務的核心挑戰在於取得一個 **有效且具備正確權限連結** 的長期 Instagram Access Token。過程中遇到了兩個主要障礙：「Error validating client secret」以及「Object with ID '...' does not exist, cannot be loaded due to missing permissions」。最終診斷出問題的根源在於 **短期 Token 缺乏關鍵權限**，導致無法正確連結到 IG 商業帳號。

## 過程紀錄與除錯步驟

### 階段一：解決「Error validating client secret」 (應用程式密鑰錯誤)

| 步驟 | 描述 | 錯誤訊息/結果 | 解決方案 |
| :--- | :--- | :--- | :--- |
| 1.1 | 使用者嘗試將短期 Token 轉換為長期 Token。 | `Error validating client secret` (code: 1) | 診斷為 `client_secret` 錯誤或短期 Token 過期。要求使用者確認 App ID/Secret，並使用 **新鮮** 的短期 Token。 |
| 1.2 | 使用者提供新的 App ID (`2586805778343847`) 和 App Secret (`4ec40cededebd3717082319f05b0ee97`)。 | 成功轉換為長期 Token。 | 確認 App ID/Secret 正確。 |

### 階段二：解決「Missing Permissions」 (權限連結錯誤)

| 步驟 | 描述 | 錯誤訊息/結果 | 解決方案 |
| :--- | :--- | :--- | :--- |
| 2.1 | 使用者使用有效的長期 Token 測試應用程式，貼文 ID 為 `DPTVMXFCScz`。 | `Unsupported get request. Object with ID 'DPTVMXFCScz' does not exist, cannot be loaded due to missing permissions...` | 診斷為 **Token 權限連結錯誤** 或 **貼文所有權問題**。要求使用者提供一個屬於自己帳號的貼文進行測試。 |
| 2.2 | 使用者確認 `DPTVMXFCScz` 確實是自己帳號的貼文。 | 錯誤持續。 | 診斷為 **Token 雖然有效，但沒有正確連結到 IG 商業帳號**。要求使用者在 Graph API Explorer 中執行 `me?fields=instagram_business_account` 進行驗證。 |
| 2.3 | 使用者執行 `me?fields=instagram_business_account`。 | `(#100) Tried accessing nonexisting field (instagram_business_account) on node type (User)` | 診斷為 **短期 Token 缺少關鍵權限** (`instagram_basic` 和 `pages_show_list`)。 |
| 2.4 | 要求使用者重新獲取包含 `instagram_basic`、`pages_show_list` 和 `instagram_manage_comments` 的短期 Token。 | 使用者提供新的短期 Token。 | 進行最終長期 Token 轉換。 |

### 階段三：最終測試與未決問題

| 步驟 | 描述 | 錯誤訊息/結果 | 狀態 |
| :--- | :--- | :--- | :--- |
| 3.1 | 使用者使用 **最新** 轉換的長期 Token 再次測試應用程式，貼文 ID 為 `DPTVMXFCScz`。 | 錯誤持續：`Object with ID 'DPTVMXFCScz' does not exist...` | **未決**。所有 Token 和權限問題已排除，問題極可能出在 **貼文本身** 無法被 IG Graph API 識別為可讀取的媒體物件。 |
| 3.2 | 建議使用者在 Graph API Explorer 中直接查詢 IG 商業帳號下的媒體列表，以確認該貼文是否存在於 API 可讀取的範圍內。 | 任務暫停。 | **待執行**。 |

## 結論

我們已經成功地排除了所有 Access Token 獲取和轉換的障礙。目前的問題已從 **Token 獲取** 轉移到 **特定貼文的 API 可讀性**。建議下一步是：

1.  **在 Graph API Explorer 中確認 IG 商業帳號 ID。**
2.  **使用 IG 商業帳號 ID 查詢媒體列表，確認 `DPTVMXFCScz` 是否在列表中。**
3.  **如果不在，則使用列表中任何一個貼文 ID 進行最終測試。**

---
*此文件為開發過程紀錄，不作為最終交付文件。*
