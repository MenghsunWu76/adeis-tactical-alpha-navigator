import streamlit as st
import pandas as pd

# ==========================================
# 1. 頁面全局設定
# ==========================================
st.set_page_config(
    page_title="ADEIS 戰術 Alpha 導航系統", 
    page_icon="🎯", 
    layout="wide"
)

# ==========================================
# 2. 標題與側邊欄 (總經與大盤環境設定)
# ==========================================
st.title("🎯 ADEIS 戰術 Alpha 導航系統")
st.markdown("結合 **總經位階 (P/E)** 與 **大盤乖離率** 的期權戰術決策中樞。")
st.markdown("---")

st.sidebar.header("🌍 宏觀環境參數輸入")
st.sidebar.markdown("請設定目前的市場位階：")

# CFO 手動輸入或未來自動抓取的參數
current_pe = st.sidebar.number_input("台股目前本益比 (P/E)", min_value=10.0, max_value=30.0, value=23.5, step=0.1)
pe_threshold = st.sidebar.slider("P/E 危險警戒線", min_value=18.0, max_value=25.0, value=22.0, step=0.5)

st.sidebar.markdown("---")
st.sidebar.header("🛡️ V25 系統防禦參數")
target_00675L_ratio = st.sidebar.slider("00675L 目標佔比 (%)", min_value=30, max_value=80, value=50, step=5)

# ==========================================
# 3. 數據匯入區塊
# ==========================================
st.subheader("📁 1. 匯入 V25 戰情數據庫")
uploaded_file = st.file_uploader("請上傳最新的 ADEIS_Backup CSV 檔案", type=['csv'])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ 戰情數據讀取成功！")
        
        # 抓取最新一筆大盤點位
        latest_index = df['Current_Index'].iloc[-1]
        
        # ==========================================
        # 4. 核心決策儀表板
        # ==========================================
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 宏觀位階判定")
            if current_pe >= pe_threshold:
                st.error(f"🚨 **高估值警戒**：目前 P/E ({current_pe}) 已超過警戒線 ({pe_threshold})！市場處於極端狂熱階段。")
            else:
                st.success(f"🟢 **安全水位**：目前 P/E ({current_pe}) 處於合理區間。")
                
            st.metric(label="最新大盤點位", value=f"{latest_index:,.2f}")
            
        with col2:
            st.subheader("⚔️ 期權戰術建議 (Alpha)")
            if current_pe >= pe_threshold:
                st.warning("⚠️ **【戰術暫停】**\n\n高位階軋空風險極高。**全面暫停賣出 Call Spread 雙向收租**。\n\n👉 建議動作：空手觀望，或僅在單日大跌 400 點以上時，於大盤下方 1000 點處 Sell PUT。")
            else:
                st.info("✅ **【常規收租】**\n\n市場估值健康。可啟動 1000 點護城河之 Iron Condor 雙向收租策略。")
                
        st.markdown("---")
        st.subheader("⚖️ V25 閥值再平衡監控 (開發中...)")
        st.info("即將載入：00675L 與 00713 佔比偏離運算，提示物理降落時機。")
            
    except Exception as e:
        st.error(f"讀取檔案時發生錯誤：{e}")
else:
    st.warning("請從上方上傳檔案以啟動 Alpha 導航雷達。")
