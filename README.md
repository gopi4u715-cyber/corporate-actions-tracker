# Stock Split Impact: Unadjusted vs Real Price Moves

A small corporate actions analysis showing what a stock split looks like in an unadjusted price feed, what actually happened in the market, and how cost basis is carried through.

**Live dashboard:** https://public.tableau.com/app/profile/gopinath.paila/viz/StockSplitImpact/StockSplitImpact

## Why I built it

Corporate actions are a common source of pricing and position breaks. A feed that doesn't adjust for a split shows a 66% to 98% "crash" on split day, which can trigger false alerts or distort returns. Cost basis has a related trap: per-share basis changes, but total basis must not. This project makes both visible.

## Data

| Item | Detail |
|---|---|
| Source | Yahoo Finance via `yfinance` |
| Screened | 12 large-cap tickers, splits since 2018 |
| Split events found | 10 events across 8 tickers (AAPL, NVDA x2, TSLA x2, AMZN, GOOGL, WMT, AVGO, CMG) |

## Method

1. **Pull splits** for each ticker (`splits.py`).
2. **Reconstruct the as-traded price.** Yahoo's Close is already adjusted for later splits (AAPL's pre-split price shows about $125 instead of the roughly $500 it traded at). I rebuilt the real price as adjusted close x split ratio x the product of any later splits, so double-split names (NVDA, TSLA) are handled (`impact.py`).
3. **Compare** the day-before and split-day prices two ways: the move an unadjusted feed would show vs the real move.
4. **Cost basis example** (`basis.py`): a hypothetical 100-share position bought just before each split. Shares multiply by the ratio, per-share basis divides by it, total basis stays the same.

## Results

| Ticker | Split date | Ratio | As-traded before | As-traded on | Unadjusted move | Real move |
|---|---|---|---|---|---|---|
| AAPL | 2020-08-31 | 4:1 | 499.23 | 129.04 | -74.2% | +3.4% |
| TSLA | 2020-08-31 | 5:1 | 2,213.40 | 498.32 | -77.5% | +12.6% |
| NVDA | 2021-07-20 | 4:1 | 751.19 | 186.12 | -75.2% | -0.9% |
| AMZN | 2022-06-06 | 20:1 | 2,447.00 | 124.79 | -94.9% | +2.0% |
| GOOGL | 2022-07-18 | 20:1 | 2,235.55 | 109.03 | -95.1% | -2.5% |
| TSLA | 2022-08-25 | 3:1 | 891.29 | 296.07 | -66.8% | -0.3% |
| WMT | 2024-02-26 | 3:1 | 175.56 | 59.60 | -66.1% | +1.8% |
| NVDA | 2024-06-10 | 10:1 | 1,208.88 | 121.79 | -89.9% | +0.7% |
| CMG | 2024-06-26 | 50:1 | 3,283.04 | 65.86 | -98.0% | +0.3% |
| AVGO | 2024-07-15 | 10:1 | 1,700.67 | 171.42 | -89.9% | +0.8% |

- An unadjusted feed shows 66% to 98% "crashes" on split day. The real moves ranged from -2.5% to +12.6%.
- TSLA's +12.6% on 2020-08-31 is a genuine market move, not a data error.

## Cost basis check

For every event, total basis before and after the split matches to within a few dollars. The small differences come from rounding per-share basis to 2 decimals. In production you would carry more precision or adjust by lot.

The `control_ok` flag compares the value change of the hypothetical position with the real price move. This is an internal consistency check on the arithmetic, not an independent verification, since both sides come from the same price data.

## Spin-off example (hypothetical numbers)

Not from real data. This illustrates how basis is allocated in a spin-off.

- Shareholder owns 100 shares of ParentCo, bought at $50 each (total basis $5,000).
- ParentCo spins off SpinCo at 1 SpinCo share per 4 ParentCo shares, so the shareholder receives 25 SpinCo shares.
- After the spin-off, ParentCo trades at $48 and SpinCo at $32.

| Holding | Shares | Price | Value | Share of total | Allocated basis | Basis per share |
|---|---|---|---|---|---|---|
| ParentCo | 100 | $48 | $4,800 | 85.71% | $4,285.71 | $42.86 |
| SpinCo | 25 | $32 | $800 | 14.29% | $714.29 | $28.57 |
| Total | | | $5,600 | 100% | $5,000.00 | |

Basis is split in proportion to fair market value after the spin-off, and the total stays at $5,000. In practice the allocation percentages come from the issuer's published tax guidance, so this is an illustration and not tax advice.

## Limitations

- Yahoo's adjustment behavior is inferred from the data (AAPL check), not from documentation I verified.
- As-traded prices are reconstructed, not checked against exchange records.
- Positions are hypothetical.
- Dividends and other corporate actions (mergers, rights issues) are not covered.

## Run it

```
pip install pandas yfinance
python splits.py     # writes splits.csv
python impact.py     # writes splits_impact.csv
python basis.py      # writes splits_basis.csv
```

Open `splits_basis.csv` in Tableau, or view the live dashboard linked above.

## Files

- `splits.py` pulls split events
- `impact.py` reconstructs as-traded prices and compares moves
- `basis.py` hypothetical cost basis and consistency check
- `splits_basis.csv` final output used in the dashboard

## Tools

Python (pandas, yfinance), Tableau Public
