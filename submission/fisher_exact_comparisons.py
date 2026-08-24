import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from itertools import combinations

df = pd.read_csv("marketing_data.csv")

# Aggregate by channel: total conversions and total clicks (attempts)
agg = df.groupby("Channel").agg(
    Conversions=("Conversions", "sum"),
    Clicks=("Clicks", "sum")
).reset_index()
agg["Non_Conversions"] = agg["Clicks"] - agg["Conversions"]
agg["Conversion_Rate"] = agg["Conversions"] / agg["Clicks"]

print("Summary table:")
print(agg.to_string(index=False))

groups = sorted(agg["Channel"].unique())
results = []

for group_a, group_b in combinations(groups, 2):
    row_a = agg[agg["Channel"] == group_a].iloc[0]
    row_b = agg[agg["Channel"] == group_b].iloc[0]

    table = [
        [row_a["Conversions"], row_a["Non_Conversions"]],
        [row_b["Conversions"], row_b["Non_Conversions"]]
    ]

    odds_ratio, p_value = stats.fisher_exact(table, alternative="two-sided")

    rate_a = row_a["Conversion_Rate"]
    rate_b = row_b["Conversion_Rate"]
    diff = rate_b - rate_a
    pct_diff = (diff / rate_a) * 100

    results.append({
        "Group_A": group_a, "Group_B": group_b,
        "Conversions_A": row_a["Conversions"], "Conversions_B": row_b["Conversions"],
        "Rate_A": round(rate_a, 4), "Rate_B": round(rate_b, 4),
        "Diff": round(diff, 4), "Pct_Diff": round(pct_diff, 1),
        "Odds_Ratio": round(odds_ratio, 3), "p_value": p_value,
        "Significant_p05": p_value < 0.05
    })

results_df = pd.DataFrame(results)
print(f"\n{results_df.to_string(index=False)}")
print(f"\nTotal comparisons: {len(results_df)}")
print(f"Significant at α=0.05: {results_df['Significant_p05'].sum()}")

results_df.to_csv("fisher_exact_results.csv", index=False)

# Bar chart of conversion rates
agg_sorted = agg.sort_values("Conversion_Rate")
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(agg_sorted["Channel"], agg_sorted["Conversion_Rate"] * 100, color="darkcyan")
for bar, rate in zip(bars, agg_sorted["Conversion_Rate"] * 100):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, f"{rate:.2f}%", va="center", fontsize=9)
ax.set_xlabel("Conversion Rate (%)")
ax.set_title("Conversion Rate by Channel")
plt.tight_layout()
plt.savefig("rate_comparison.png", dpi=150)
print("\nSaved rate_comparison.png")