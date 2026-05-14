import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("📊 Market Risk & Volatility Dashboard")

import os

BASE_DIR = os.path.dirname(__file__)
csv_path = os.path.join(BASE_DIR, "market_data.csv")

data = pd.read_csv(csv_path, index_col="Date", parse_dates=True)


data["Daily_Return"] = data["Close"].pct_change()
data.dropna(inplace=True)
data["Volatility_20D"] = data["Daily_Return"].rolling(20).std()

# ---- Metrics ----
mean_return = data["Daily_Return"].mean()
volatility = data["Daily_Return"].std()

st.metric("Mean Daily Return", round(mean_return,5))
st.metric("Daily Volatility", round(volatility,5))

# ---- Plot Returns ----
st.subheader("Daily Returns")
st.line_chart(data["Daily_Return"])

# ---- Plot Volatility ----
st.subheader("20-Day Rolling Volatility")
st.line_chart(data["Volatility_20D"])

# ---- Monte Carlo ----
st.subheader("Monte Carlo Simulation")

last_price = data["Close"].iloc[-1]
simulations = 200
days = 30

results = np.zeros((days, simulations))

for i in range(simulations):
    price = last_price
    for d in range(days):
        price *= (1 + np.random.normal(mean_return, volatility))
        results[d, i] = price

fig, ax = plt.subplots()
ax.plot(results, alpha=0.3)
st.pyplot(fig)

expected_price = results[-1].mean()
st.metric("Expected Price (30 days)", round(expected_price,2))

# ---- VaR ----
VaR = np.percentile(data["Daily_Return"], 5)
st.metric("Value at Risk (95%)", round(VaR,5))
