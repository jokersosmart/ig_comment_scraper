# 📖 Instagram 貼文留言爬蟲工具：使用者操作手冊

**作者**: Manus AI  
**版本**: 1.0  
**日期**: 2025 年 11 月 3 日

---

## 📝 應用程式概述

**Instagram 貼文留言爬蟲工具** 是一個基於 Streamlit 框架開發的網頁應用程式，旨在協助您輕鬆、安全地爬取指定 Instagram 公開貼文的所有留言，並將結果匯出為結構化的 Excel 檔案，以便進行後續的數據分析和商品改良。

本工具的設計遵循 Instagram Graph API 的使用規範，確保您的操作符合平台政策。

### 核心功能一覽

| 功能 | 說明 |
| :--- | :--- |
| **安全授權** | 透過使用者自行輸入 Access Token 進行授權，Token 不會被保存或記錄。 |
| **貼文識別** | 支援透過完整的 **貼文 URL** 或 **Post ID** 來指定目標貼文。 |
| **留言爬取** | 呼叫 Instagram Graph API 獲取留言內容、留言人資訊、時間戳記和讚數。 |
| **數據分析** | 實時顯示總留言數、平均讚數、獨特使用者數等統計資訊。 |
| **Excel 匯出** | 將所有爬取到的留言數據格式化並匯出為 `.xlsx` 檔案。 |

---

## 🔧 前置要求

在使用本工具之前，您需要完成以下準備工作：

### 1. Instagram 帳號類型

請注意，Instagram Graph API 僅支援以下帳號類型：

*   ✅ **Business Account** (商業帳號)
*   ✅ **Creator Account** (創作者帳號)
*   ❌ **Personal Account** (個人帳號) **不支援**

### 2. 獲取 Access Token

您必須擁有一個有效的 **Instagram Graph API Access Token**。

1.  **訪問 Facebook for Developers**：前往 [https://developers.facebook.com/](https://developers.facebook.com/)。
2.  **建立應用程式**：建立一個新的應用程式，並新增「**Instagram Graph API**」產品。
3.  **產生 Token**：透過 Graph API Explorer 或其他方式，為您的 Instagram 帳號產生一個 Access Token。

> **重要安全提示**：Access Token 是您帳號的鑰匙。本工具設計為在每次運行時要求您輸入，且不會在伺服器端保存。請妥善保管您的 Token，並在完成操作後考慮撤銷或更新。

---

## 🚀 操作步驟指南

無論您是在本地運行 (`streamlit run app.py`) 還是使用 Streamlit Cloud 部署的線上版本，操作介面和步驟都是一致的。

### 步驟 1：訪問應用程式

在您的網頁瀏覽器中打開應用程式的 URL (例如：`http://localhost:8501` 或您的 Streamlit Cloud 網址)。

### 步驟 2：輸入驗證資訊

在頁面左側的「**📋 驗證資訊**」區塊，您會看到一個密碼輸入框：

*   **🔑 Instagram Access Token**：請將您準備好的 Access Token 貼入此處。
    *   輸入完成後，下方會顯示 `✅ Token 已輸入` 的成功訊息。

### 步驟 3：輸入貼文資訊

在頁面右側的「**🔗 貼文資訊**」區塊，選擇您希望輸入貼文資訊的方式：

1.  **選擇輸入方式**：
    *   **貼文 URL**：選擇此項，並在下方輸入框貼上完整的 Instagram 貼文連結 (例如：`https://www.instagram.com/p/ABC123XYZ/`)。
    *   **Post ID**：選擇此項，並在下方輸入框輸入貼文的唯一識別碼 (例如：`ABC123XYZ`)。
2.  **確認 Post ID**：無論您選擇哪種方式，系統都會嘗試解析並顯示 `✅ Post ID: [您的 ID]` 的確認訊息。

### 步驟 4：開始爬取留言

*   點擊頁面中央的 **「🚀 開始爬取留言」** 按鈕。
*   應用程式將開始連接 Instagram API，並在頁面上顯示進度：
    *   `⏳ 正在連接 Instagram API...`
    *   `📥 正在爬取留言... 已獲取 [N] 條 (第 [M] 頁)`
*   請耐心等待，直到爬取完成。

### 步驟 5：查看結果與下載

爬取成功後，頁面會顯示 `✅ 爬取成功！` 的訊息，並在下方顯示結果：

1.  **📋 數據預覽**：
    *   顯示爬取到的留言數據表格，您可以直接在網頁上瀏覽。
2.  **📈 統計資訊**：
    *   提供總留言數、平均讚數、最多讚數等關鍵統計指標。
    *   顯示留言讚數分佈的直方圖。
3.  **💾 下載文件**：
    *   切換到此分頁，點擊 **「📥 下載 Excel 檔案」** 按鈕。
    *   檔案名稱格式為 `comments_YYYYMMDD_HHMMSS.xlsx`。
    *   下載的 Excel 檔案包含所有留言的詳細資訊，包括：`序號`、`留言人帳號`、`留言人名稱`、`留言人 ID`、`留言內容`、`留言時間`、`留言讚數`、`留言 ID`、`貼文 ID`。

---

## ⚠️ 常見問題與排查

| 問題 | 可能原因 | 解決方案 |
| :--- | :--- | :--- |
| **「❌ API 錯誤: Invalid OAuth access token」** | Access Token 無效、過期或複製不完整。 | 重新到 Facebook Developer 平台申請新的 Access Token，並確保完整複製。 |
| **「❌ API 錯誤: Post ID not found」** | 貼文 ID 錯誤，或貼文不是公開的。 | 檢查貼文 URL 或 Post ID 是否正確，並確認貼文是公開狀態。 |
| **「❌ API 錯誤: Rate limit exceeded」** | 短時間內發送過多請求，超過 Instagram API 的配額限制 (通常為每小時 200 個請求)。 | 等待一段時間 (建議 1 小時) 後再重試。 |
| **「❌ 請求超時」** | 網路連接不穩定或 API 伺服器響應慢。 | 檢查您的網路連接，或稍後再試。 |
| **無法下載 Excel 檔案** | 瀏覽器設定或快取問題。 | 嘗試清除瀏覽器快取，或更換其他瀏覽器。 |

---

## 附錄：技術細節

本工具使用的主要技術棧和 API 資訊：

| 項目 | 說明 |
| :--- | :--- |
| **開發語言** | Python 3.9+ |
| **網頁框架** | Streamlit |
| **數據處理** | Pandas |
| **Excel 處理** | openpyxl |
| **API 端點** | `https://graph.instagram.com/v18.0/{post_id}/comments` |
| **API 欄位** | `id,from,text,timestamp,like_count` |

---

**祝您使用愉快！**
