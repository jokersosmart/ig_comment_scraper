# 極度詳細：Instagram 長期 Access Token 獲取指南

## 概述
本指南將詳細說明如何為您的 Streamlit 留言爬蟲工具獲取一個 **有效且具備正確權限連結** 的 Instagram 長期 Access Token。這個 Token 是使用 Meta Graph API 爬取您 **IG 商業帳號** 貼文留言的唯一憑證。

**重要限制**：Meta Graph API 僅允許您爬取 **您自己的 IG 商業帳號** 下的貼文留言。

## 前置準備 (Prerequisites)

在開始之前，請確保您已完成以下準備工作：

1.  **Meta 開發者帳號**：您已擁有一個 Meta 開發者帳號。
2.  **Meta 應用程式**：您已在 Meta 開發者後台創建了一個應用程式 (App ID: `2586805778343847`)。
3.  **IG 商業帳號**：您的 Instagram 帳號已切換為 **專業帳號 (商業帳號)**。
4.  **FB 粉絲專頁連結**：您的 IG 商業帳號已正確連結到一個 **Facebook 粉絲專頁**。

## 步驟一：獲取短期 Access Token (Short-Lived Token)

我們將使用 **圖形 API 總管 (Graph API Explorer)** 來獲取一個包含所有必要權限的短期 Token。

1.  **開啟圖形 API 總管**：
    *   前往 [https://developers.facebook.com/tools/explorer/](https://developers.facebook.com/tools/explorer/)

2.  **選擇應用程式**：
    *   在頁面右上方，確認 **「Meta 應用程式」** 下拉選單中選擇了您的應用程式 (`V1` 或 App ID: `2586805778343847`)。

3.  **選擇權限 (Permissions)**：
    *   點擊 **「新增權限」**，並在列表中 **務必勾選** 以下三個關鍵權限：
        *   **`instagram_basic`**：允許讀取 IG 商業帳號的基本資訊。
        *   **`pages_show_list`**：允許讀取您管理的粉絲專頁列表 (這是連結 IG 帳號的橋樑)。
        *   **`instagram_manage_comments`**：允許讀取 IG 貼文留言 (這是爬蟲工具的核心權限)。

4.  **產生存取權杖 (Generate Access Token)**：
    *   點擊 **「產生存取權杖」** 按鈕。
    *   **重要**：系統會彈出視窗要求您授權。請務必：
        *   **選擇** **已連結到您的 IG 商業帳號** **的那個 Facebook 粉絲專頁**。
        *   **授權** 所有要求的權限。

5.  **複製短期 Token**：
    *   成功後，您會在 **「存取權杖」** 欄位中看到一串新的 Token。這就是您的 **短期 Access Token** (有效期限約 1 小時)。

## 步驟二：轉換為長期 Access Token (Long-Lived Token)

短期 Token 很快就會過期，我們需要將其轉換為 **長期 Token** (有效期限約 60 天)。

1.  **準備轉換網址**：
    *   請使用以下格式的網址進行轉換，並替換三個參數：
        *   `[CLIENT_ID]`：您的應用程式編號 (`2586805778343847`)。
        *   `[CLIENT_SECRET]`：您的應用程式密鑰 (請在 Meta 開發者後台 **「設定」->「基本」** 中獲取)。
        *   `[SHORT_LIVED_TOKEN]`：您在步驟一中獲取的短期 Access Token。

    \`\`\`
    https://graph.facebook.com/v20.0/oauth/access_token?
      grant_type=fb_exchange_token&           
      client_id=[CLIENT_ID]&
      client_secret=[CLIENT_SECRET]&
      fb_exchange_token=[SHORT_LIVED_TOKEN]
    \`\`\`

2.  **執行轉換**：
    *   將完整的網址貼到您的瀏覽器中訪問。

3.  **獲取長期 Token**：
    *   您將獲得一個 JSON 回應，其中 `access_token` 欄位的值就是您的 **長期 Access Token**。
    *   範例回應：
        \`\`\`json
        {
          "access_token": "EAAkwr6eFZA6cBP...",
          "token_type": "bearer",
          "expires_in": 5184000 // 約 60 天
        }
        \`\`\`

## 步驟三：驗證 Token 連結 (關鍵除錯步驟)

在應用程式中使用 Token 之前，請先在 Graph API Explorer 中驗證它是否已正確連結到您的 IG 商業帳號。

1.  **在 Graph API Explorer 中使用長期 Token**：
    *   將您在步驟二中獲得的 **長期 Access Token** 貼到 Graph API Explorer 的 **「存取權杖」** 欄位。

2.  **查詢 IG 商業帳號 ID**：
    *   在網址欄位輸入：`me?fields=instagram_business_account`
    *   點擊 **「送出」**。

3.  **預期結果**：
    *   **成功**：您將獲得一個 JSON 回應，其中包含您的 IG 商業帳號 ID。
        \`\`\`json
        {
          "instagram_business_account": {
            "id": "17841400000000000" // 您的 IG 商業帳號 ID
          },
          "id": "100000000000000" // 您的 FB 使用者 ID
        }
        \`\`\`
    *   **失敗**：如果出現 `(#100) Tried accessing nonexisting field (instagram_business_account)...`，請回到步驟一，確認您已勾選 **`instagram_basic`** 和 **`pages_show_list`**，並選擇了 **正確的 FB 粉絲專頁**。

## 常見錯誤與解決方案

| 錯誤訊息 | 原因 | 解決方案 |
| :--- | :--- | :--- |
| **Error validating client secret** | 應用程式密鑰錯誤，或短期 Token 已過期。 | 1. 確認 App Secret 複製正確。 2. 重新獲取一個 **新鮮** 的短期 Token (步驟一)。 |
| **Object with ID '...' does not exist, cannot be loaded due to missing permissions** | **Token 缺少關鍵權限** 或 **未正確連結到 IG 商業帳號**。 | 1. 確保短期 Token 包含 **`instagram_basic`** 和 **`pages_show_list`** 權限 (步驟一)。 2. 確保在授權時選擇了 **正確的 FB 粉絲專頁** (步驟一)。 3. **確認貼文本身** 在 Graph API Explorer 的媒體列表中可見 (步驟三)。 |
| **(#100) Tried accessing nonexisting field (instagram_business_account)...** | Token 缺少讀取 IG 商業帳號資訊的權限。 | 回到步驟一，**務必勾選 `instagram_basic` 和 `pages_show_list`**。 |

---

