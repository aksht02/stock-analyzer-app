import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Stock Price Analyzer", layout="centered")

st.title("📊 STOCK PRICE ANALYZER")
st.write("Check live stock prices using Yahoo Finance")

# ---------------- FUNCTION ----------------
def get_stock_data(symbol):
    ticker = yf.Ticker(symbol)
    info = ticker.info
    hist = ticker.history(period="1mo")

    company_name = info.get("longName", symbol)
    current_price = info.get("currentPrice")
    previous_close = info.get("previousClose")
    high_52 = info.get("fiftyTwoWeekHigh")
    low_52 = info.get("fiftyTwoWeekLow")

    if current_price and previous_close:
        change = current_price - previous_close
        pct_change = (change / previous_close) * 100
        daily_change = f"{change:+.2f} ({pct_change:+.2f}%)"
    else:
        daily_change = "N/A"

    return company_name, current_price, daily_change, high_52, low_52, hist


# ---------------- INPUT ----------------
symbol = st.text_input("Enter stock symbol (e.g. TSLA, RELIANCE.NS)")

if st.button("Fetch Stock Data"):

    if symbol:
        with st.spinner("Fetching data..."):
            company, price, change, high_52, low_52, hist = get_stock_data(symbol.upper())

        st.success("Stock data loaded successfully!")

        st.subheader(company)

        col1, col2 = st.columns(2)

        col1.metric("Current Price", f"${price:,.2f}" if price else "N/A")
        col2.metric("Daily Change", change)

        st.markdown("### 📌 52-Week Range")
        st.write(f"High: ${high_52}")
        st.write(f"Low: ${low_52}")

        # 📈 Chart
        st.markdown("### 📈 Last 30 Days Price Chart")
        st.line_chart(hist["Close"])

        # 💾 Download CSV
        csv = hist.to_csv().encode("utf-8")
        st.download_button(
            label="Download Last 30 Days Data (CSV)",
            data=csv,
            file_name=f"{symbol}_data.csv",
            mime="text/csv",
        )

    else:
        st.warning("Please enter a stock symbol")
        st.markdown(
    """
    <hr>
    <div style="text-align: center; font-size:14px; opacity:0.6;">
        Created by <b>Akshay Tak</b> 🚀 | 
        <a href="https://github.com/aksht02" target="_blank">GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)

