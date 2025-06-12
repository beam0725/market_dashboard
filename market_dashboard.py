
import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="全球市場數據儀表板", layout="wide")
st.title("📊 全球市場數據儀表板")

# 國家與市場指數、債券殖利率對應
data_categories = {
    "股市指數": {
        "美國": {
            "S&P 500": "^GSPC",
            "Nasdaq": "^IXIC",
            "道瓊工業指數": "^DJI"
        },
        "台灣": {
            "加權指數": "^TWII"
        }
    },
    "債券殖利率": {
        "美國": {
            "10年期公債殖利率": "^TNX",
            "2年期公債殖利率": "^IRX"
        }
    }
}

# 類別選擇
category = st.selectbox("選擇資料類別", list(data_categories.keys()))

# 國家選擇
selected_country = st.selectbox("選擇國家", list(data_categories[category].keys()))

# 日期範圍選擇
date_range = st.date_input("選擇日期區間", value=[pd.to_datetime("2023-01-01"), pd.to_datetime("today")])
start_date = date_range[0].strftime("%Y-%m-%d")
end_date = date_range[1].strftime("%Y-%m-%d")

# 顯示資料
st.subheader(f"{selected_country} - {category} 資料")
for name, ticker in data_categories[category][selected_country].items():
    df = yf.download(ticker, start=start_date, end=end_date)
    if not df.empty:
        latest_value = df['Close'].iloc[-1]
        latest_date = df.index[-1].strftime('%Y-%m-%d')
        st.metric(label=f"{name} 最新數值（{latest_date}）", value=round(latest_value, 2))
        st.line_chart(df['Close'], height=300, use_container_width=True)
    else:
        st.warning(f"無法取得 {name} 的資料")
