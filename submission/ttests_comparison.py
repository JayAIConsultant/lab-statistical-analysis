import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from itertools import combinations

df = pd.read_csv("marketing_data.csv")

metric = "Row_CPA"
clean = df[["Channel", metric]].replace([np.inf, -np.inf], np.nan).dropna()
groups = sorted(clean["Channel"].unique())

results = []
for group_a, group_b in combinations(groups, 2):
    vals_a = clean[clean["Channel"] == group_a][metric]
    vals_b = clean[clean["Channel"] == group_b][metric]

    t_stat, p_value = stats.ttest_ind(vals_a, vals_b, equal_var=False)  # Welch's t-test

    mean_a, mean_b = vals_a.mean(), vals_b.mean()
    diff = mean_b - mean_a
    pct_diff = (diff / mean_a) * 100

    pooled_std = np.sqrt((vals_a.var() + vals_b.var()) / 2)
    cohens_d = diff / pooled_std

    if abs(cohens_d) < 0.2:
        effect = "negligible"
    elif abs(cohens_d) < 0.5:
        effect = "small"
    elif abs(cohens_d) < 0.8:
        effect = "medium"
    else:
        effect = "large"

    results.append({
        "Group_A": group_a, "Group_B": group_b,
        "Mean_A": round(mean_a, 2), "Mean_B": round(mean_b, 2),
        "Diff": round(diff, 2), "Pct_Diff": round(pct_diff, 1),
        "t_stat": round(t_stat, 3), "p_value": p_value,
        "Cohens_d": round(cohens_d, 3), "Effect_Size": effect,
        "Significant_p05": p_value < 0.05
    })

results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))
print(f"\nTotal comparisons: {len(results_df)}")
print(f"Significant at α=0.05: {results_df['Significant_p05'].sum()}")

results_df.to_csv("cpa_ttest_results.csv", index=False)

# Heatmap of p-values
n = len(groups)
p_matrix = np.ones((n, n))
for _, row in results_df.iterrows():
    i, j = groups.index(row["Group_A"]), groups.index(row["Group_B"])
    p_matrix[i, j] = row["p_value"]
    p_matrix[j, i] = row["p_value"]

fig, ax = plt.subplots(figsize=(8, 7))
im = ax.imshow(p_matrix, cmap="RdYlGn_r", vmin=0, vmax=0.1)
ax.set_xticks(range(n)); ax.set_xticklabels(groups, rotation=45, ha="right")
ax.set_yticks(range(n)); ax.set_yticklabels(groups)
for i in range(n):
    for j in range(n):
        ax.text(j, i, f"{p_matrix[i,j]:.3f}", ha="center", va="center", fontsize=8)
plt.colorbar(im, label="p-value")
plt.title("CPA Comparison: p-values (Welch's t-test)")
plt.tight_layout()
plt.savefig("metric_comparison_heatmap.png", dpi=150)
print("\nSaved metric_comparison_heatmap.png")