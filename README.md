# 多平台留言爬蟲工具 (Multi-Platform Comment Scraper)

## 專案概述
本專案是一個基於 Streamlit 框架開發的多平台留言爬蟲工具，旨在提供一個統一的介面，讓使用者能夠輕鬆地從 Instagram (IG)、Facebook (FB)、YouTube 和 Matters (方格子) 爬取貼文留言，並將結果匯出為標準化的 Excel 檔案。

### 支援平台與技術
| 平台 | 技術 | 備註 |
| :--- | :--- | :--- |
| **Instagram (IG)** | Meta Graph API | 需要長期 Access Token，僅限爬取 **使用者自己的 IG 商業帳號** 下的貼文留言。 |
| **Facebook (FB)** | Meta Graph API | 需要長期 Access Token，用於爬取 FB 粉絲專頁貼文留言。 |
| **YouTube** | YouTube Data API v3 | 需要 API Key，用於爬取影片留言。 |
| **Matters (方格子)** | Web Scraping | 使用網頁爬蟲技術，無需 API 憑證。 |

### 核心功能
*   **統一介面**：使用者只需輸入貼文網址，應用程式會自動判斷平台。
*   **智慧憑證提示**：只有在需要 API 憑證的平台 (IG, FB, YouTube) 才會提示使用者輸入。
*   **標準化匯出**：所有平台爬取的資料將統一格式，匯出為 Excel 檔案。

## 執行步驟 (Execution Guide)

### 步驟一：環境準備
1.  **複製專案**：
    \`\`\`bash
    git clone https://github.com/jokersosmart/ig_comment_scraper.git
    cd ig_comment_scraper
    \`\`\`
2.  **安裝依賴**：
    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`

### 步驟二：憑證獲取 (IG/FB/YouTube)
*   **YouTube**：請前往 Google Cloud Console 獲取 **YouTube Data API v3 Key**。
*   **Instagram/Facebook**：請參閱 **[IG_Token_Acquisition_Guide.md](./IG_Token_Acquisition_Guide.md)** 獲取 **長期 Access Token**。

### 步驟三：啟動應用程式
在專案根目錄下執行：
\`\`\`bash
streamlit run app.py
\`\`\`
應用程式將在瀏覽器中開啟 (預設為 `http://localhost:8501`)。

### 步驟四：使用與測試
1.  在應用程式介面中輸入貼文網址。
2.  輸入所需的 API 憑證 (IG/FB/YouTube) 或留空 (Matters)。
3.  點擊 **「🚀 開始爬取留言」**。
4.  爬取完成後，點擊 **「下載 Excel 檔案」** 獲取結果。

## 開發與除錯紀錄
本次開發過程中，針對 **Instagram Access Token** 的獲取與權限連結進行了大量的除錯工作。詳細的除錯過程、錯誤訊息與解決方案，請參閱：
*   **[IG_Token_Acquisition_Log.md](./IG_Token_Acquisition_Log.md)**

---
*本專案由 Manus AI 協助開發與維護。*
