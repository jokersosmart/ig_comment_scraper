# 🚀 Instagram 貼文留言爬蟲工具：環境準備與部署指南

**作者**: Manus AI  
**版本**: 1.0  
**日期**: 2025 年 11 月 3 日

---

## 📝 引言

本指南旨在提供一個完整的流程，協助您部署和運行 **Instagram 貼文留言爬蟲工具**。此工具基於 Streamlit 框架，使用 **Instagram Graph API** 爬取指定貼文的留言，並將結果匯出為 Excel 檔案，以利於您進行使用者體驗回饋分析和商品改良。

**核心功能**：
*   **使用者授權**：透過使用者自行輸入 Access Token 進行授權。
*   **資料爬取**：支援透過貼文 URL 或 Post ID 爬取留言。
*   **資料匯出**：將爬取結果匯出為格式化的 Excel (.xlsx) 檔案。
*   **網頁介面**：提供 Streamlit 網頁應用程式介面，方便操作和部署。

---

## 📋 第一部分：環境準備清單

在開始部署之前，請確保您的環境符合以下要求，並完成必要的準備工作。

### 1. 軟體要求

| 軟體 | 版本要求 | 備註 |
| :--- | :--- | :--- |
| **Python** | 3.9 或更高版本 | 建議使用最新穩定版 |
| **Git** | 最新版本 | 用於版本控制和部署到 Streamlit Cloud |
| **網頁瀏覽器** | Chrome, Firefox, Edge 等 | 用於運行 Streamlit 應用程式 |

### 2. 帳號準備

| 帳號/資源 | 目的 | 獲取方式 |
| :--- | :--- | :--- |
| **Instagram 帳號** | 必須是 **Business Account** 或 **Creator Account** | 個人帳號 (Personal Account) 不支援 Graph API |
| **Facebook Developer 帳號** | 用於建立應用程式和獲取 Access Token | 訪問 [Facebook for Developers](https://developers.facebook.com/) |
| **GitHub 帳號** | 用於程式碼託管和 Streamlit Cloud 部署 | 訪問 [GitHub](https://github.com/) |
| **Streamlit Cloud 帳號** | 用於免費託管網頁應用程式 | 訪問 [Streamlit Cloud](https://streamlit.io/cloud) |

### 3. 獲取 Instagram Access Token

這是工具運行的關鍵步驟。您需要透過 Facebook Developer 平台獲取一個有效的 Access Token。

1.  **建立 Facebook 應用程式**：
    *   登入 [Facebook for Developers](https://developers.facebook.com/)。
    *   建立一個新的應用程式，選擇類型為「**消費者**」或「**商業**」。
    *   在應用程式儀表板中，新增「**Instagram Graph API**」產品。
2.  **獲取 Token**：
    *   進入「**工具**」→「**Graph API Explorer**」。
    *   選擇您的應用程式和 Instagram 帳號。
    *   確保您已選擇必要的權限，例如 `instagram_basic` 和 `instagram_manage_comments` (或類似的讀取權限)。
    *   點擊「**產生 Access Token**」並將其複製保存。

> **安全提示**：Access Token 具有敏感性，請勿將其硬寫在程式碼中或上傳到 GitHub。本工具設計為讓使用者在運行時輸入，確保安全。

---

## 🛠️ 第二部分：本地環境設定與運行

本工具的程式碼已準備就緒，您只需按照以下步驟在本地環境中安裝依賴並運行。

### 1. 建立專案資料夾與檔案

請在您的電腦上建立一個名為 `ig_scraper` 的資料夾，並將以下兩個檔案放入其中：

*   `app.py` (應用程式核心程式碼)
*   `requirements.txt` (Python 依賴清單)

#### `requirements.txt` 內容

```
streamlit==1.28.1
pandas==2.0.3
openpyxl==3.11.0
requests==2.31.0
```

#### `app.py` 內容

由於程式碼較長，請參考您提供的原始 `app.py` 檔案內容。它包含 Streamlit 介面、API 呼叫邏輯 (`fetch_comments`) 和 Excel 匯出邏輯 (`export_to_excel`)。

### 2. 安裝依賴

請使用終端機進入 `ig_scraper` 資料夾，並執行以下步驟：

1.  **建立並啟動虛擬環境** (強烈建議)：
    ```bash
    # 建立虛擬環境
    python3 -m venv venv
    
    # 啟動虛擬環境 (macOS/Linux)
    source venv/bin/activate
    
    # 啟動虛擬環境 (Windows)
    .\venv\Scripts\activate
    ```
2.  **安裝 Python 依賴**：
    ```bash
    pip install -r requirements.txt
    ```

### 3. 運行應用程式

安裝完成後，您可以使用 Streamlit 運行應用程式：

```bash
streamlit run app.py
```

應用程式將會在您的預設瀏覽器中開啟 (通常是 `http://localhost:8501`)。

---

## ☁️ 第三部分：部署到 Streamlit Cloud

Streamlit Cloud 提供了一個免費且簡單的方式來託管您的應用程式。

### 1. 準備 GitHub 倉庫

1.  **建立 GitHub 倉庫**：在 GitHub 上建立一個新的公開或私有倉庫，例如 `ig_scraper`。
2.  **上傳程式碼**：將 `ig_scraper` 資料夾中的所有檔案 (包括 `app.py` 和 `requirements.txt`) 上傳到您的 GitHub 倉庫。

```bash
# 在 ig_scraper 資料夾內執行
git init
git add .
git commit -m "Initial commit for IG Comment Scraper"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ig_scraper.git # 替換為您的倉庫 URL
git push -u origin main
```

### 2. 部署到 Streamlit Cloud

1.  **登入 Streamlit Cloud**：訪問 [Streamlit Cloud](https://streamlit.io/cloud) 並使用您的 GitHub 帳號登入。
2.  **新建應用**：點擊「**New app**」按鈕。
3.  **配置部署選項**：
    *   **Repository**: 選擇您剛才建立的 `ig_scraper` 倉庫。
    *   **Branch**: 選擇 `main`。
    *   **Main file path**: 輸入 `app.py`。
4.  **點擊「Deploy」**：Streamlit Cloud 將會自動安裝依賴並運行您的應用程式。
5.  **獲取應用 URL**：部署完成後，您將獲得一個公開的應用程式 URL (例如：`https://YOUR_USERNAME-ig-scraper.streamlit.app`)，您可以將此 URL 分享給其他使用者。

---

## 💡 第四部分：應用程式使用說明

應用程式運行後，使用者可以按照以下步驟操作：

1.  **訪問應用程式**：打開本地運行 (http://localhost:8501) 或 Streamlit Cloud 部署的 URL。
2.  **輸入 Access Token**：在左側的「**驗證資訊**」區塊，輸入您的 Instagram Access Token。
3.  **輸入貼文資訊**：
    *   選擇「**貼文 URL**」並貼上完整的 Instagram 貼文連結。
    *   或選擇「**Post ID**」並輸入貼文的唯一識別碼。
4.  **開始爬取**：點擊頁面中央的「**🚀 開始爬取留言**」按鈕。
5.  **等待結果**：應用程式將顯示進度條和已爬取的留言數量。
6.  **下載 Excel**：爬取完成後，切換到「**💾 下載文件**」分頁，點擊「**📥 下載 Excel 檔案**」按鈕即可保存結果。

---

## 附錄：檔案結構

您的專案資料夾結構應如下所示：

```
ig_scraper/
├── app.py              # 應用程式核心程式碼
├── requirements.txt    # Python 依賴清單
└── deployment_guide_final.md # 本部署指南
└── venv/               # 虛擬環境 (本地運行時產生)
```
