import pandas as pd
import numpy as np
from scipy.stats import false_discovery_control
import matplotlib.pyplot as plt

cpa_results = pd.read_csv("cpa_ttest_results.csv")
fisher_results = pd.read_csv("fisher_exact_results.csv")

n_cpa = len(cpa_results)
n_fisher = len(fisher_results)
total_comparisons = n_cpa + n_fisher

print(f"Total comparisons across both families: {total_comparisons}")
print(f"Expected false positives at α=0.05 by chance alone: {total_comparisons * 0.05:.2f}")
print()

# --- Bonferroni ---
alpha = 0.05
alpha_bonf_cpa = alpha / n_cpa
alpha_bonf_fisher = alpha / n_fisher

cpa_results["significant_bonferroni"] = cpa_results["p_value"] < alpha_bonf_cpa
fisher_results["significant_bonferroni"] = fisher_results["p_value"] < alpha_bonf_fisher

print(f"Bonferroni-adjusted alpha (CPA, n={n_cpa}): {alpha_bonf_cpa:.5f}")
print(f"CPA comparisons significant after Bonferroni: {cpa_results['significant_bonferroni'].sum()} / {n_cpa}")
print(cpa_results[cpa_results["significant_bonferroni"]][["Group_A", "Group_B", "p_value"]].to_string(index=False))
print()

print(f"Bonferroni-adjusted alpha (Conversion Rate, n={n_fisher}): {alpha_bonf_fisher:.5f}")
print(f"Fisher comparisons significant after Bonferroni: {fisher_results['significant_bonferroni'].sum()} / {n_fisher}")
print(fisher_results[fisher_results["significant_bonferroni"]][["Group_A", "Group_B", "p_value"]].to_string(index=False))
print()

# --- Benjamini-Hochberg FDR ---
cpa_results["p_value_fdr"] = false_discovery_control(cpa_results["p_value"], method="bh")
cpa_results["significant_fdr"] = cpa_results["p_value_fdr"] < alpha

fisher_results["p_value_fdr"] = false_discovery_control(fisher_results["p_value"], method="bh")
fisher_results["significant_fdr"] = fisher_results["p_value_fdr"] < alpha

print(f"CPA comparisons significant after FDR: {cpa_results['significant_fdr'].sum()} / {n_cpa}")
print(cpa_results[cpa_results["significant_fdr"]][["Group_A", "Group_B", "p_value", "p_value_fdr"]].to_string(index=False))
print()

print(f"Fisher comparisons significant after FDR: {fisher_results['significant_fdr'].sum()} / {n_fisher}")
print(fisher_results[fisher_results["significant_fdr"]][["Group_A", "Group_B", "p_value", "p_value_fdr"]].to_string(index=False))

cpa_results.to_csv("cpa_ttest_results.csv", index=False)
fisher_results.to_csv("fisher_exact_results.csv", index=False)

# --- Comparison summary + chart ---
summary = pd.DataFrame({
    "Method": ["Uncorrected (a=0.05)", "Bonferroni", "FDR (Benjamini-Hochberg)"],
    "CPA_Significant": [
        (cpa_results["p_value"] < 0.05).sum(),
        cpa_results["significant_bonferroni"].sum(),
        cpa_results["significant_fdr"].sum()
    ],
    "ConversionRate_Significant": [
        (fisher_results["p_value"] < 0.05).sum(),
        fisher_results["significant_bonferroni"].sum(),
        fisher_results["significant_fdr"].sum()
    ]
})
print("\nCorrection method comparison:")
print(summary.to_string(index=False))
summary.to_csv("correction_comparison_summary.csv", index=False)

fig, ax = plt.subplots(figsize=(8, 5))
x = np.arange(len(summary))
width = 0.35
ax.bar(x - width/2, summary["CPA_Significant"], width, label="CPA (t-test)", color="steelblue")
ax.bar(x + width/2, summary["ConversionRate_Significant"], width, label="Conversion Rate (Fisher)", color="darkorange")
ax.set_xticks(x)
ax.set_xticklabels(summary["Method"], rotation=15, ha="right")
ax.set_ylabel("Number of Significant Comparisons")
ax.set_title("Effect of Multiple Comparisons Correction")
ax.legend()
plt.tight_layout()
plt.savefig("correction_comparison.png", dpi=150)
print("\nSaved correction_comparison.png")