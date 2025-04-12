import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import matplotlib.pyplot as plt

st.set_page_config(page_title="RSI & SMA Assistant", layout="centered")

st.title("AI Trading Assistant (RSI + SMA Strategy)")

# Input
symbol = st.text_input("Enter Stock Symbol", value="AAPL")

if st.button("Get Signal"):
    try:
        data = yf.download(symbol, period="6mo", interval="1d")

        if data.empty:
            st.error(f"No data found for {symbol}")
        else:
            # Extract close series directly as a Series (not ndarray!)
            close_series = data["Close"].dropna()

            # Apply indicators
            rsi_series = ta.momentum.RSIIndicator(close_series, window=14).rsi()
            sma_series = ta.trend.SMAIndicator(close_series, window=20).sma_indicator()

            # Align everything on the same index
            data = pd.DataFrame({
                "Close": close_series,
                "RSI": rsi_series,
                "SMA": sma_series
            }).dropna()

            # DEBUG OUTPUT
            st.subheader("Debug Data Snapshot")
            st.write(data.tail())

            # Signals
            data["Signal"] = "HOLD"
            data.loc[(data["RSI"] < 30) & (data["Close"] > data["SMA"]), "Signal"] = "BUY"
            data.loc[(data["RSI"] > 70) & (data["Close"] < data["SMA"]), "Signal"] = "SELL"

            latest = data.iloc[-1]
            st.markdown(f"### Latest Signal for **{symbol.upper()}**: `{latest['Signal']}`")
            st.markdown(f"**Closing Price:** {latest['Close']:.2f} | **RSI:** {latest['RSI']:.2f} | **SMA:** {latest['SMA']:.2f}")

            # Charts
            st.subheader("Price & SMA")
            fig1, ax1 = plt.subplots()
            ax1.plot(data["Close"], label="Price")
            ax1.plot(data["SMA"], label="SMA (20)", linestyle="--")
            ax1.legend()
            st.pyplot(fig1)

            st.subheader("RSI Chart")
            fig2, ax2 = plt.subplots()
            ax2.plot(data["RSI"], label="RSI", color="purple")
            ax2.axhline(70, color="red", linestyle="--")
            ax2.axhline(30, color="green", linestyle="--")
            ax2.legend()
            st.pyplot(fig2)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
