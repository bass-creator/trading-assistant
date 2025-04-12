# Streamlit RSI + SMA Trading Assistant
import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import matplotlib.pyplot as plt

st.set_page_config(page_title="RSI & SMA Assistant", layout="centered")
st.title("AI Trading Assistant (RSI + SMA Strategy)")

# Stock input
symbol = st.text_input("Enter Stock Symbol", value="AAPL")

if st.button("Get Signal"):
    try:
        st.write(f"Fetching data for {symbol.upper()}...")
        data = yf.download(symbol, period="6mo", interval="1d")
        
        if data.empty:
            st.error(f"No data found for {symbol}. Try another symbol.")
        else:
            close_series = data[['Close']].copy()  # Keep as DataFrame for compatibility
            close_series = close_series.droplevel(axis=1, level=0) if isinstance(close_series.columns, pd.MultiIndex) else close_series

            # Flatten Close to Series
            close_series = close_series.squeeze()  # Works if it's a one-column DataFrame

            # Calculate RSI and SMA
            data['RSI'] = ta.momentum.RSIIndicator(close_series, window=14).rsi()
            data['SMA'] = ta.trend.SMAIndicator(close_series, window=20).sma_indicator()

            # Signal logic
            buy = (data['RSI'] < 30) & (data['Close'] > data['SMA'])
            sell = (data['RSI'] > 70) & (data['Close'] < data['SMA'])
            data['Signal'] = "HOLD"
            data.loc[buy, "Signal"] = "BUY"
            data.loc[sell, "Signal"] = "SELL"

            latest = data.dropna().iloc[-1]

            st.markdown(f"### Latest Signal for **{symbol.upper()}**: `{latest['Signal']}`")
            st.markdown(f"**Close:** {latest['Close']:.2f} | **RSI:** {latest['RSI']:.2f} | **SMA:** {latest['SMA']:.2f}")

            # Price & SMA plot
            st.subheader("Price & SMA")
            fig1, ax1 = plt.subplots()
            ax1.plot(data.index, data['Close'], label="Price")
            ax1.plot(data.index, data['SMA'], label="20-Day SMA", linestyle="--")
            ax1.legend()
            st.pyplot(fig1)

            # RSI plot
            st.subheader("RSI")
            fig2, ax2 = plt.subplots()
            ax2.plot(data.index, data['RSI'], color="purple")
            ax2.axhline(70, color="red", linestyle="--")
            ax2.axhline(30, color="green", linestyle="--")
            st.pyplot(fig2)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
