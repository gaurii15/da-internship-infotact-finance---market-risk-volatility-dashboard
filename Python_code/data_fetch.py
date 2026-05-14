

import yfinance as yf

ticker = "AAPL"
start_date = "2022-01-01"
end_date = "2025-01-01"

data = yf.download(ticker, start=start_date, end=end_date)

# Clean column names
data.columns = data.columns.get_level_values(0)

# Preview data
print(data.head())

# Save data
data.to_csv("market_data.csv")

