import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("marketing_data.csv")

# Aggregate by Channel: sum raw counts, then derive ratio metrics from the sums
# (sum-then-derive, not average-of-ratios, to avoid the sum-then-round bug pattern)
agg = df.groupby("Channel").agg(
    Impressions=("Impressions", "sum"),
    Clicks=("Clicks", "sum"),
    Conversions=("Conversions", "sum"),
    Cost=("Cost", "sum"),
    Revenue=("Revenue", "sum"),
).reset_index()

agg["CTR"] = agg["Clicks"] / agg["Impressions"]
agg["Conversion_Rate"] = agg["Conversions"] / agg["Clicks"]
agg["CPA"] = agg["Cost"] / agg["Conversions"]
agg["ROAS"] = agg["Revenue"] / agg["Cost"]
agg["Profit"] = agg["Revenue"] - agg["Cost"]
agg["Profit_Margin"] = agg["Profit"] / agg["Revenue"]

agg = agg.replace([np.inf, -np.inf], np.nan)

print(agg.round(2).to_string(index=False))
agg.to_csv("group_metrics_summary.csv", index=False)

# Visualization
fig, axes = plt.subplots(3, 2, figsize=(12, 12))

agg.sort_values("CPA").plot.barh(x="Channel", y="CPA", ax=axes[0, 0], legend=False, color="steelblue")
axes[0, 0].set_title("CPA by Channel")

agg.sort_values("ROAS").plot.barh(x="Channel", y="ROAS", ax=axes[0, 1], legend=False, color="seagreen")
axes[0, 1].set_title("ROAS by Channel")

agg.sort_values("Conversion_Rate").plot.barh(x="Channel", y="Conversion_Rate", ax=axes[1, 0], legend=False, color="coral")
axes[1, 0].set_title("Conversion Rate by Channel")

agg.sort_values("Conversions").plot.barh(x="Channel", y="Conversions", ax=axes[1, 1], legend=False, color="mediumpurple")
axes[1, 1].set_title("Total Conversions by Channel")

agg.sort_values("Cost").plot.barh(x="Channel", y="Cost", ax=axes[2, 0], legend=False, color="goldenrod")
axes[2, 0].set_title("Total Cost by Channel")

agg.sort_values("Profit").plot.barh(x="Channel", y="Profit", ax=axes[2, 1], legend=False, color="teal")
axes[2, 1].axvline(0, color="black", linewidth=0.8)
axes[2, 1].set_title("Profit by Channel")

plt.tight_layout()
plt.savefig("group_metrics_overview.png", dpi=150)
print("\nSaved group_metrics_overview.png")