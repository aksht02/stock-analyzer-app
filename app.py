import streamlit as st
import yfinance as yf

# ---------- FUNCTION ----------
def get_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        company_name = info.get("longName", symbol)
        current_price = info.get("currentPrice")
        previous_close = info.get("previousClose")

        if current_price is not None and previous_close is not None:
            change = current_price - previous_close
            pct_change = (change / previous_close) * 100
            daily_change = f"{change:+.2f} ({pct_change:+.2f}%)"
        else:
            daily_change = "N/A"

        return {
            "Company Name": company_name,
            "Current Price": current_price,
            "Daily Change": daily_change
        }

    except Exception as e:
        st.error(f"Error: {e}")
        return None


# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="Stock Analyzer", layout="centered")

st.title("📈 Stock Analyzer")
st.markdown("Check live stock prices using **Yahoo Finance**")

symbol = st.text_input(
    "Enter stock symbol (e.g. AAPL, TCS.NS, RELIANCE.NS)",
    placeholder="AAPL"
)

if st.button("Fetch Stock Data"):
    if symbol:
        with st.spinner("Fetching stock data..."):
            data = get_stock_data(symbol.upper())

        if data:
            st.success("Stock data loaded successfully!")

            st.subheader(data["Company Name"])

            col1, col2 = st.columns(2)

            col1.metric(
                label="Current Price",
                value=f"₹{data['Current Price']:,.2f}" if data["Current Price"] else "N/A"
            )

            col2.metric(
                label="Daily Change",
                value=data["Daily Change"]
            )
    else:
        st.warning("Please enter a stock symbol")
