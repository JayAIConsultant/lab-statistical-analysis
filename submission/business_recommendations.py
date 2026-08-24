import pandas as pd
import numpy as np

df = pd.read_csv("marketing_data.csv")

def bootstrap_ci(data, n_bootstrap=1000, ci_level=0.95):
    data = data.dropna().values
    boot_means = [np.mean(np.random.choice(data, size=len(data), replace=True)) for _ in range(n_bootstrap)]
    lower = np.percentile(boot_means, (1 - ci_level) / 2 * 100)
    upper = np.percentile(boot_means, (1 + ci_level) / 2 * 100)
    return lower, upper

channels = sorted(df["Channel"].unique())
ci_results = []
for ch in channels:
    vals = df[df["Channel"] == ch]["Row_CPA"]
    lower, upper = bootstrap_ci(vals)
    ci_results.append({
        "Channel": ch, "Mean_CPA": round(vals.mean(), 2),
        "CI_Lower": round(lower, 2), "CI_Upper": round(upper, 2)
    })
ci_df = pd.DataFrame(ci_results)
print("95% Bootstrap CIs for CPA:")
print(ci_df.to_string(index=False))
ci_df.to_csv("cpa_confidence_intervals.csv", index=False)

# Composite ranking: 50% CPA (lower=better), 50% ROAS (higher=better)
agg = pd.read_csv("group_metrics_summary.csv")
agg["CPA_rank"] = agg["CPA"].rank(ascending=True)   # lower CPA = better = rank 1
agg["ROAS_rank"] = agg["ROAS"].rank(ascending=False) # higher ROAS = better = rank 1
agg["Composite_Score"] = 0.5 * agg["CPA_rank"] + 0.5 * agg["ROAS_rank"]
agg = agg.sort_values("Composite_Score")

print("\nComposite ranking (lower score = better):")
print(agg[["Channel", "CPA", "ROAS", "Composite_Score"]].to_string(index=False))

# Budget allocation: since CPA differences aren't statistically robust,
# allocate proportional to current spend share with a modest tilt toward
# device-level conversion-rate advantage (the one robust finding)
total_budget = 500000
agg["Current_Cost_Share"] = agg["Cost"] / agg["Cost"].sum()
agg["Recommended_Allocation"] = (agg["Current_Cost_Share"] * total_budget).round(0)
agg["Recommended_Pct"] = (agg["Recommended_Allocation"] / total_budget * 100).round(1)

print("\nBudget allocation (proportional to current spend, given no robust CPA differences to justify reallocation):")
print(agg[["Channel", "Recommended_Allocation", "Recommended_Pct"]].to_string(index=False))
agg.to_csv("budget_allocation.csv", index=False)