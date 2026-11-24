import pandas as pd, yfinance as yf

splits = pd.read_csv("splits.csv", parse_dates=["date"])
rows = []
for t, g in splits.groupby("ticker"):
    px = yf.download(t, start="2019-12-01", end="2026-11-01",
                     auto_adjust=False, progress=False, threads=False)
    close = px["Close"].squeeze()
    close.index = pd.to_datetime(close.index).tz_localize(None)
    for _, s in g.iterrows():
        later = g[g.date > s.date].ratio.prod()      # splits that happen after this one
        before_date = close[close.index < s.date].index[-1]
        on_date = close[close.index >= s.date].index[0]
        adj_before, adj_on = close[before_date], close[on_date]
        as_before = adj_before * s.ratio * later     # real price the day before the split
        as_on = adj_on * later                       # real price on split day
        rows.append({
            "ticker": t, "split_date": s.date.date(), "ratio": s.ratio,
            "as_traded_before": round(as_before, 2),
            "as_traded_on": round(as_on, 2),
            "unadjusted_move_pct": round((as_on / as_before - 1) * 100, 1),
            "real_move_pct": round((adj_on / adj_before - 1) * 100, 1),
            "shares_per_100_after": int(100 * s.ratio),
            "basis_per_share_factor": round(1 / s.ratio, 4),
        })

out = pd.DataFrame(rows).sort_values(["ticker", "split_date"])
out.to_csv("splits_impact.csv", index=False)
print(out.to_string(index=False))
