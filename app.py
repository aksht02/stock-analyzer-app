import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

st.set_page_config(page_title="Advanced Stock Dashboard", layout="wide")

st.title("📊 ADVANCED STOCK PRICE ANALYZER")
st.write("Live stock tracking using Yahoo Finance API")

# ---------------- MARKET STATUS ----------------
def get_market_status():
    india = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india)
    hour = now.hour

    if 9 <= hour < 15:
        return "🟢 Market Open"
    else:
        return "🔴 Market Closed"

st.sidebar.markdown("### Market Status")
st.sidebar.success(get_market_status())

# ---------------- INPUT SECTION ----------------
symbols_input = st.text_input(
    "Enter stock symbols separated by comma (e.g. TSLA, AAPL, RELIANCE.NS)"
)

period = st.selectbox(
    "Select Time Period",
    ["1mo", "3mo", "6mo", "1y", "5y"]
)

# ---------------- FUNCTION ----------------
def get_stock_data(symbol, period):
    ticker = yf.Ticker(symbol)
    info = ticker.info
    hist = ticker.history(period=period)

    company = info.get("longName", symbol)
    current_price = info.get("currentPrice")
    previous_close = info.get("previousClose")
    logo = info.get("logo_url")

    if current_price and previous_close:
        change = current_price - previous_close
        pct = (change / previous_close) * 100
    else:
        change = 0
        pct = 0

    return company, current_price, change, pct, hist, logo


# ---------------- BUTTON ACTION ----------------
if st.button("Analyze Stocks"):

    if symbols_input:
        symbols = [s.strip().upper() for s in symbols_input.split(",")]

        comparison_data = []

        for symbol in symbols:
            company, price, change, pct, hist, logo = get_stock_data(symbol, period)

            st.markdown("---")
            col_logo, col_data = st.columns([1, 3])

            # Company Logo
            if logo:
                col_logo.image(logo, width=80)

            col_data.subheader(company)

            # Color change based on gain/loss
            if change >= 0:
                color = "green"
            else:
                color = "red"

            col1, col2 = st.columns(2)

            col1.metric(
                "Current Price",
                f"${price:,.2f}" if price else "N/A",
                delta=f"{change:+.2f} ({pct:+.2f}%)"
            )

            # Chart
            st.line_chart(hist["Close"])

            # Save for comparison table
            comparison_data.append({
                "Symbol": symbol,
                "Price": price,
                "Change": round(change, 2),
                "% Change": round(pct, 2)
            })

        # ---------------- COMPARISON TABLE ----------------
        st.markdown("## 📊 Stock Comparison Table")
        df = pd.DataFrame(comparison_data)
        st.dataframe(df)

    else:
        st.warning("Please enter at least one stock symbol.")
