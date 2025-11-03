import streamlit as st
import requests
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from datetime import datetime
import re
import time
from io import BytesIO

# ═══════════════════════════════════════════════════════════
# 頁面配置
# ═══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="IG 留言爬蟲工具",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自訂 CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("📱 Instagram 貼文留言爬蟲工具")
st.markdown("**版本 1.0** | 輕鬆爬取 IG 留言並匯出 Excel")
st.markdown("---")

# ═══════════════════════════════════════════════════════════
# 側邊欄 - 使用說明
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.header("📖 使用指南")
    
    with st.expander("🔧 前置準備", expanded=True):
        st.markdown("""
        **您需要準備：**
        1. **Instagram 帳號類型**
           - Business Account ✅
           - Creator Account ✅
           - Personal Account ❌ (不支援)
        
        2. **Access Token**
           - 訪問 https://developers.facebook.com/
           - 建立應用並申請 Token
        
        3. **貼文資訊**
           - Instagram 公開貼文 URL
           - 或貼文的 Post ID
        """)
    
    with st.expander("⚙️ 操作步驟"):
        st.markdown("""
        **3 個簡單步驟：**
        
        **步驟 1️⃣** - 輸入 Access Token
        - 在上方輸入框貼入您的 Token
        
        **步驟 2️⃣** - 輸入貼文資訊
        - 提供貼文完整 URL 或 Post ID
        
        **步驟 3️⃣** - 開始爬取
        - 點擊「🚀 開始爬取留言」按鈕
        - 等待完成後下載 Excel
        """)
    
    with st.expander("⚠️ 常見問題"):
        st.markdown("""
        **Q: 我的帳號支援嗎？**
        A: 只有 Business 或 Creator 帳號支援。
        
        **Q: Token 如何申請？**
        A: 訪問 Facebook Developer 官方文件。
        
        **Q: 為什麼無法爬取？**
        A: 確保貼文是公開的。
        
        **Q: 配額有限制嗎？**
        A: 免費層每小時 200 個請求。
        """)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; font-size: 12px; color: #999;'>
        💡 <b>提示</b>: 此工具遵循 Instagram API 使用政策
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# 輔助函數
# ═══════════════════════════════════════════════════════════

@st.cache_data
def extract_post_id(url: str) -> str:
    """從 IG URL 提取 Post ID"""
    try:
        # 支援格式: https://www.instagram.com/p/{post_id}/
        #          https://www.instagram.com/reel/{post_id}/
        match = re.search(r'/(p|reel|tv)/([A-Za-z0-9_-]+)/', url)
        if match:
            return match.group(2)
    except:
        pass
    return None

def fetch_comments(access_token: str, post_id: str, fields: str = "id,from,text,timestamp,like_count") -> list:
    """
    使用 Instagram Graph API 獲取留言
    
    參數:
    - access_token: Instagram Access Token
    - post_id: 貼文 ID
    - fields: 要獲取的欄位
    
    返回值:
    - 留言列表或 None (如果出錯)
    """
    url = f"https://graph.instagram.com/v18.0/{post_id}/comments"
    
    comments = []
    after = None
    progress_bar = st.progress(0)
    status_placeholder = st.empty()
    
    try:
        page_count = 0
        while True:
            params = {
                'access_token': access_token,
                'fields': fields,
                'limit': 100  # 每次獲取 100 條
            }
            
            if after:
                params['after'] = after
            
            # 更新進度訊息
            status_placeholder.info(f"📥 正在爬取留言... 已獲取 {len(comments)} 條 (第 {page_count + 1} 頁)")
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code != 200:
                error_data = response.json().get('error', {})
                error_msg = error_data.get('message', f'HTTP {response.status_code}')
                st.error(f"❌ API 錯誤: {error_msg}")
                return None
            
            data = response.json()
            
            if 'data' not in data:
                break
            
            comments.extend(data['data'])
            page_count += 1
            
            # 更新進度條
            progress = min(page_count / 10, 1.0)  # 假設最多 10 頁
            progress_bar.progress(progress)
            
            # 添加延遲以避免速率限制
            time.sleep(0.5)
            
            # 檢查是否有下一頁
            if 'paging' in data and 'cursors' in data['paging'] and 'after' in data['paging']['cursors']:
                after = data['paging']['cursors']['after']
            else:
                break
        
        progress_bar.progress(1.0)
        status_placeholder.success(f"✅ 成功獲取 {len(comments)} 條留言！")
        
        return comments
    
    except requests.exceptions.Timeout:
        st.error("❌ 請求超時，請檢查網路連接")
        return None
    except requests.exceptions.ConnectionError:
        st.error("❌ 無法連接到 Instagram API")
        return None
    except Exception as e:
        st.error(f"❌ 發生錯誤: {str(e)}")
        return None

def format_comments_to_dataframe(comments: list, post_id: str) -> pd.DataFrame:
    """將留言資料轉換為 DataFrame"""
    
    formatted_data = []
    
    for idx, comment in enumerate(comments, 1):
        formatted_data.append({
            '序號': idx,
            '留言人帳號': comment.get('from', {}).get('username', 'N/A'),
            '留言人名稱': comment.get('from', {}).get('name', 'N/A'),
            '留言人 ID': comment.get('from', {}).get('id', 'N/A'),
            '留言內容': comment.get('text', ''),
            '留言時間': comment.get('timestamp', ''),
            '留言讚數': comment.get('like_count', 0),
            '留言 ID': comment.get('id', ''),
            '貼文 ID': post_id
        })
    
    df = pd.DataFrame(formatted_data)
    
    # 轉換時間格式為更易讀的形式
    try:
        df['留言時間'] = pd.to_datetime(df['留言時間']).dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        pass
    
    return df

def export_to_excel(df: pd.DataFrame, filename: str = "comments.xlsx"):
    """將 DataFrame 匯出為 Excel 並返回位元組"""
    
    # 使用 pandas 寫入 Excel
    
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='留言數據')
        
        # 獲取 worksheet
        worksheet = writer.sheets['留言數據']
        
        # 設置欄寬
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)  # 最大寬度 50
            worksheet.column_dimensions[column_letter].width = adjusted_width
        
        # 設置表頭格式
        header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        
        for cell in worksheet[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
        # 凍結表頭
        worksheet.freeze_panes = "A2"
    
    output.seek(0)
    return output.getvalue()

# ═══════════════════════════════════════════════════════════
# 主應用邏輯
# ═══════════════════════════════════════════════════════════

st.markdown("""
### 🔒 安全提示
- Access Token 不會被保存或記錄
- 每次頁面重新加載後即被清空
- 爬取的數據僅用於本次操作
""")

st.markdown("---")

# 建立兩欄布局
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 驗證資訊")
    access_token = st.text_input(
        "🔑 Instagram Access Token",
        type="password",
        help="您的 Instagram Graph API Access Token（密碼欄位隱藏輸入）"
    )
    
    token_status = st.empty()
    if access_token:
        token_status.success(f"✅ Token 已輸入 ({len(access_token)} 字符)")

with col2:
    st.subheader("🔗 貼文資訊")
    input_type = st.radio("選擇輸入方式", ["貼文 URL", "Post ID"], horizontal=True)
    
    if input_type == "貼文 URL":
        post_input = st.text_input(
            "📱 貼文 URL",
            placeholder="https://www.instagram.com/p/ABC123XYZ/",
            help="完整的 Instagram 貼文連結"
        )
        post_id = extract_post_id(post_input) if post_input else None
        if post_id:
            st.success(f"✅ Post ID: {post_id}")
    else:
        post_id = st.text_input(
            "🆔 Post ID",
            placeholder="ABC123XYZ",
            help="貼文的唯一識別碼"
        )
        if post_id:
            st.success(f"✅ Post ID: {post_id}")

st.markdown("---")

# 爬取按鈕
col_button = st.columns([1, 1, 1])

with col_button[1]:
    if st.button("🚀 開始爬取留言", use_container_width=True, type="primary"):
        
        # 驗證輸入
        if not access_token:
            st.error("❌ 請輸入 Access Token")
            st.stop()
        elif not post_id:
            st.error("❌ 請輸入有效的貼文 URL 或 Post ID")
            st.stop()
        else:
            # 建立容器來管理進度顯示
            progress_container = st.container()
            
            with progress_container:
                st.info("⏳ 正在連接 Instagram API...")
            
            # 呼叫 API 獲取留言
            comments = fetch_comments(access_token, post_id)
            
            if comments is not None:
                # 轉換為 DataFrame
                df = format_comments_to_dataframe(comments, post_id)
                
                # 清除進度容器
                progress_container.empty()
                
                # 顯示成功訊息
                st.markdown("""
                <div class='success-box'>
                    <h3>✅ 爬取成功！</h3>
                    爬取的留言資料已準備好下載。
                </div>
                """, unsafe_allow_html=True)
                
                # 顯示預覽
                st.subheader(f"📊 爬取結果 ({len(df)} 條留言)")
                
                # 建立分頁選項卡
                tab1, tab2, tab3 = st.tabs(["📋 數據預覽", "📈 統計資訊", "💾 下載文件"])
                
                with tab1:
                    # 顯示資料表
                    st.dataframe(
                        df,
                        use_container_width=True,
                        height=400,
                        column_config={
                            "序號": st.column_config.NumberColumn(width="small"),
                            "留言讚數": st.column_config.NumberColumn(width="small"),
                            "留言內容": st.column_config.TextColumn(width="large"),
                        }
                    )
                
                with tab2:
                    # 統計資訊
                    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                    
                    with col_stat1:
                        st.metric("🗣️ 總留言數", len(df))
                    
                    with col_stat2:
                        avg_likes = df['留言讚數'].mean()
                        st.metric("❤️ 平均讚數", f"{avg_likes:.1f}")
                    
                    with col_stat3:
                        max_likes = df['留言讚數'].max()
                        st.metric("⭐ 最多讚", max_likes)
                    
                    with col_stat4:
                        min_likes = df['留言讚數'].min()
                        st.metric("📍 最少讚", min_likes)
                    
                    # 額外統計
                    st.markdown("---")
                    col_extra1, col_extra2 = st.columns(2)
                    
                    with col_extra1:
                        st.write("**留言人統計**")
                        unique_users = df['留言人帳號'].nunique()
                        st.metric("獨特使用者數", unique_users)
                    
                    with col_extra2:
                        st.write("**時間統計**")
                        st.metric("爬取時間", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    
                    # 留言讚數分佈圖表
                    st.markdown("---")
                    st.write("**留言讚數分佈**")
                    
                    # 建立直方圖
                    chart_data = df['留言讚數'].value_counts().sort_index()
                    st.bar_chart(chart_data)
                
                with tab3:
                    # 匯出為 Excel
                    filename = f"comments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                    excel_data = export_to_excel(df, filename)
                    
                    # 下載按鈕
                    st.download_button(
                        label="📥 下載 Excel 檔案",
                        data=excel_data,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                    
                    st.markdown("""
                    <div class='info-box'>
                    💾 <b>檔案說明</b><br>
                    - 檔案格式：Microsoft Excel (.xlsx)<br>
                    - 包含所有留言資訊<br>
                    - 可在 Excel、Google Sheets 等應用中開啟
                    </div>
                    """, unsafe_allow_html=True)

# 頁面底部 - 頁腳
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #999; font-size: 12px; padding: 2rem 0;'>
    <p>
    ✨ <b>Instagram 貼文留言爬蟲工具</b> v1.0 ✨<br>
    此工具遵循 Instagram API 使用政策，僅爬取公開資訊。<br>
    📧 有任何問題？請聯繫技術支援。
    </p>
</div>
""", unsafe_allow_html=True)
