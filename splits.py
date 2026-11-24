import pandas as pd, yfinance as yf

tickers = ["AAPL","NVDA","TSLA","AMZN","GOOGL","WMT","AVGO","CMG","KO","JNJ","XOM","MSFT"]
rows = []
for t in tickers:
    s = yf.Ticker(t).splits
    s = s[s.index >= "2018-01-01"]
    for d, r in s.items():
        rows.append({"ticker": t, "date": pd.to_datetime(d).tz_localize(None).date(), "ratio": r})

df = pd.DataFrame(rows)
df.to_csv("splits.csv", index=False)
print(df.to_string())
