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
    data = yf.download(symbol, period="6mo", interval="1d")
    data["RSI"] = ta.momentum.RSIIndicator(data["Close"], window=14).rsi()
    data["SMA"] = ta.trend.SMAIndicator(data["Close"], window=20).sma_indicator()

    buy = (data["RSI"] < 30) & (data["Close"] > data["SMA"])
    sell = (data["RSI"] > 70) & (data["Close"] < data["SMA"])
    data["Signal"] = "HOLD"
    data.loc[buy, "Signal"] = "BUY"
    data.loc[sell, "Signal"] = "SELL"

    latest = data.iloc[-1]
    st.markdown(f"### Latest Signal for **{symbol.upper()}**: `{latest['Signal']}`")

    # Show price chart
    st.subheader("Price & SMA")
    fig1, ax1 = plt.subplots()
    ax1.plot(data["Close"], label="Price")
    ax1.plot(data["SMA"], label="20-Day SMA", linestyle="--")
    ax1.legend()
    st.pyplot(fig1)

    # Show RSI chart
    st.subheader("RSI")
    fig2, ax2 = plt.subplots()
    ax2.plot(data["RSI"], color="purple")
    ax2.axhline(70, color="red", linestyle="--")
    ax2.axhline(30, color="green", linestyle="--")
    st.pyplot(fig2)
