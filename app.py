import streamlit as st
import yfinance as yf
import pandas_ta as ta

# వెబ్‌సైట్ సెట్టింగ్స్
st.set_page_config(page_title="My Trading Dashboard", layout="wide")
st.title("📊 లైవ్ స్టాక్ మార్కెట్ డాష్‌బోర్డ్")
st.write("ఇది నా స్వంత ఆల్గో-ట్రేడింగ్ వెబ్‌సైట్!")

# మనం వాడే స్టాక్స్
stocks =["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "SBIN.NS", "INFY.NS", "ITC.NS", "TATAMOTORS.NS"]

selected_stock = st.sidebar.selectbox("స్టాక్ ఎంచుకోండి (Select Stock):", stocks)
st.write(f"### 📈 {selected_stock.replace('.NS', '')} లైవ్ డేటా")

try:
    df = yf.download(selected_stock, period="3mo", interval="1d", progress=False)
    if not df.empty:
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['Prev_High'] = df['High'].shift(1)
        
        current_price = float(df['Close'].iloc[-1])
        current_rsi = float(df['RSI'].iloc[-1])
        prev_high = float(df['Prev_High'].iloc[-1])
        
        signal = "NEUTRAL 🟡"
        if current_price > prev_high and current_rsi > 50:
            signal = "STRONG BUY 🟢"
        elif current_rsi < 40:
            signal = "SELL 🔴"
            
        col1, col2, col3 = st.columns(3)
        col1.metric("ప్రస్తుత ధర", f"₹{current_price:.2f}")
        col2.metric("RSI", f"{current_rsi:.2f}")
        col3.metric("ఆల్గో సిగ్నల్", signal)
        
        st.write("### 📉 గత 3 నెలల చార్ట్")
        st.line_chart(df['Close'])
    else:
        st.warning("డేటా అందుబాటులో లేదు.")
except Exception as e:
    st.error(f"ఎర్రర్: {e}")
