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
        st.info(f"Fetching data for {symbol.upper()}...")
        data = yf.download(symbol, period="6mo", interval="1d")

        if data.empty:
            st.error(f"No data found for {symbol.upper()}. Try another symbol.")
        else:
            # Use 'Close' column as-is (just drop NAs)
            close = data["Close"].dropna()

            # Calculate RSI and SMA
            rsi = ta.momentum.RSIIndicator(close, window=14)
            data["RSI"] = rsi.rsi()

            sma = ta.trend.SMAIndicator(close, window=20)
            data["SMA"] = sma.sma_indicator()

            # Generate signals
            buy = (data["RSI"] < 30) & (data["Close"] > data["SMA"])
            sell = (data["RSI"] > 70) & (data["Close"] < data["SMA"])
            data["Signal"] = "HOLD"
            data.loc[buy, "Signal"] = "BUY"
            data.loc[sell, "Signal"] = "SELL"

            latest = data.dropna().iloc[-1]
            st.markdown(f"### Latest Signal for **{symbol.upper()}**: `{latest['Signal']}`")
            st.write(f"**Closing Price:** {latest['Close']:.2f}")
            st.write(f"**RSI:** {latest['RSI']:.2f}")
            st.write(f"**SMA:** {latest['SMA']:.2f}")

            # Plot price and SMA
            st.subheader("Price & SMA")
            fig1, ax1 = plt.subplots()
            ax1.plot(data["Close"], label="Close Price")
            ax1.plot(data["SMA"], label="20-Day SMA", linestyle="--")
            ax1.legend()
            st.pyplot(fig1)

            # Plot RSI
            st.subheader("RSI")
            fig2, ax2 = plt.subplots()
            ax2.plot(data["RSI"], label="RSI", color="purple")
            ax2.axhline(70, color="red", linestyle="--")
            ax2.axhline(30, color="green", linestyle="--")
            ax2.legend()
            st.pyplot(fig2)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
