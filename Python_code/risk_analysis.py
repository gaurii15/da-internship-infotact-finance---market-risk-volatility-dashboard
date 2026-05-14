import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------ LOAD DATA ------------------
data = pd.read_csv("market_data.csv", index_col="Date", parse_dates=True)

# ------------------ RETURNS & VOLATILITY ------------------
data["Daily_Return"] = data["Close"].pct_change()
data.dropna(inplace=True)

#20 day rollig volatility (risk indicator)
data["Volatility_20D"] = data["Daily_Return"].rolling(window=20).std()

print(data[["Daily_Return", "Volatility_20D"]].head(25))

# ------------------ PLOT 1: RETURNS & VOLATILITY ------------------
fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

axes[0].plot(data["Daily_Return"])
axes[0].set_title("Daily Returns of Apple Stock")
axes[0].set_ylabel("Daily Return")

axes[1].plot(data["Volatility_20D"])
axes[1].set_title("20-Day Rolling Volatility")
axes[1].set_ylabel("Volatility")
axes[1].set_xlabel("Date")

plt.show()
plt.close()   # ✅ prevents GUI blocking

# ------------------ MONTE CARLO SIMULATION ------------------
num_simulations = 500
num_days = 30

last_price = data["Close"].iloc[-1]
mean_return = data["Daily_Return"].mean()
std_return = data["Daily_Return"].std()

simulation_results = np.zeros((num_days, num_simulations))

for i in range(num_simulations):
    price = last_price
    for day in range(num_days):
        price *= (1 + np.random.normal(mean_return, std_return))
        simulation_results[day, i] = price

# ------------------ PLOT 2: MONTE CARLO ------------------
plt.figure(figsize=(12, 5))
plt.plot(simulation_results, alpha=0.3)
plt.title("Monte Carlo Simulation: 30-Day Price Forecast")
plt.xlabel("Days")
plt.ylabel("Stock Price")
plt.show()
plt.close()   # ✅ prevents freeze

# ------------------ EXPECTED PRICE ------------------
expected_price = simulation_results[-1].mean()
print("Expected Price after 30 days:", round(expected_price, 2))

# ------------------ VALUE AT RISK (VaR) ------------------
confidence_level = 0.95

VaR = np.percentile(
    data["Daily_Return"].dropna(),
    (1 - confidence_level) * 100
)

print("Value at Risk (95% confidence level):", round(VaR, 5))

#SUMMARY METRICS
print("\n--- SUMMARY METRICS ---")
print("Mean Daily Return:", round(mean_return, 5))
print("Daily Volatility:", round(std_return, 5))
print("Expected Price after 30 days:", round(expected_price, 2))
print("Value at Risk (95%):", round(VaR, 5))
