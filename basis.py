import pandas as pd

d = pd.read_csv("splits_impact.csv")
d["shares_before"] = 100
d["total_basis_before"] = (d.shares_before * d.as_traded_before).round(2)
d["shares_after"] = d.shares_before * d.ratio
d["basis_per_share_after"] = (d.as_traded_before / d.ratio).round(2)
d["total_basis_after"] = (d.shares_after * d.basis_per_share_after).round(2)
d["value_after"] = (d.shares_after * d.as_traded_on).round(2)
d["value_change_pct"] = ((d.value_after / d.total_basis_before - 1) * 100).round(1)
d["control_ok"] = (d.value_change_pct - d.real_move_pct).abs() < 0.2
d.to_csv("splits_basis.csv", index=False)
print(d[["ticker","split_date","ratio","shares_after","basis_per_share_after",
         "total_basis_before","total_basis_after","value_change_pct","real_move_pct","control_ok"]].to_string(index=False))
