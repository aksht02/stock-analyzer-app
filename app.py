import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from datetime import datetime
import pytz

st.set_page_config(
    page_title="Akshay Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📊 STOCK PRICE ANALYZER")
st.write("Search and track live stock prices using Yahoo Finance")

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

# ---------------- SEARCH FUNCTION ----------------
def search_stock(query):
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}"
    response = requests.get(url)
    data = response.json()

    results = []
    for item in data.get("quotes", []):
        symbol = item.get("symbol")
        name = item.get("shortname") or item.get("longname")
        if symbol and name:
            results.append(f"{name} ({symbol})")

    return results

# ---------------- STOCK DATA FUNCTION ----------------
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

# ---------------- INPUT SECTION ----------------
search_query = st.text_input("Search stock (e.g. Tesla, Reliance)")

selected_symbol = None

if search_query:
    options = search_stock(search_query)

    if options:
        selected_option = st.selectbox("Select Stock", options)
        selected_symbol = selected_option.split("(")[-1].replace(")", "")
    else:
        st.warning("No matching stocks found")

period = st.selectbox(
    "Select Time Period",
    ["1mo", "3mo", "6mo", "1y", "5y"]
)

# ---------------- BUTTON ----------------
if st.button("Analyze Stock"):

    if selected_symbol:

        company, price, change, pct, hist, logo = get_stock_data(selected_symbol, period)

        st.success("Stock data loaded successfully!")

        col_logo, col_data = st.columns([1, 3])

        if logo:
            col_logo.image(logo, width=80)

        col_data.subheader(company)

        col1, col2 = st.columns(2)

        col1.metric(
            "Current Price",
            f"${price:,.2f}" if price else "N/A",
            delta=f"{change:+.2f} ({pct:+.2f}%)"
        )

        col2.metric(
            "Daily Change %",
            f"{pct:+.2f}%"
        )

        st.markdown("### 📈 Price Chart")
        st.line_chart(hist["Close"])

        # Comparison Table
        comparison_data = {
            "Symbol": selected_symbol,
            "Price": price,
            "Change": round(change, 2),
            "% Change": round(pct, 2)
        }

        st.markdown("### 📊 Stock Summary")
        st.dataframe(pd.DataFrame([comparison_data]))

    else:
        st.warning("Please search and select a stock.")

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <div style="text-align: center; font-size:14px; opacity:0.6;">
        Created by <b>Akshay Tak</b> 🚀 |
        <a href="https://github.com/aksht02" target="_blank"> GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)
