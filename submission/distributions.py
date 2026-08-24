import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("marketing_data.csv")

# Row-level metrics, computed per observation (not from group totals) —
# this is what feeds the t-tests in Step 4, since we need per-row variability
df["Row_CPA"] = df["Cost"] / df["Conversions"]
df["Row_Conversion_Rate"] = df["Conversions"] / df["Clicks"]
df["Row_ROAS"] = df["Revenue"] / df["Cost"]

df = df.replace([np.inf, -np.inf], np.nan)

print("Row-level metric summary by Channel:")
print(df.groupby("Channel")[["Row_CPA", "Row_Conversion_Rate", "Row_ROAS"]].describe().round(3))

df.to_csv("marketing_data.csv", index=False)  # save with row-level metrics added

# Distribution plots
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for channel in df["Channel"].unique():
    subset = df[df["Channel"] == channel]
    axes[0].hist(subset["Row_CPA"].dropna(), alpha=0.4, label=channel, bins=10)
    axes[1].hist(subset["Row_Conversion_Rate"].dropna(), alpha=0.4, label=channel, bins=10)
    axes[2].hist(subset["Row_ROAS"].dropna(), alpha=0.4, label=channel, bins=10)

axes[0].set_title("CPA Distribution by Channel")
axes[0].legend(fontsize=7)
axes[1].set_title("Conversion Rate Distribution by Channel")
axes[1].legend(fontsize=7)
axes[2].set_title("ROAS Distribution by Channel")
axes[2].legend(fontsize=7)

plt.tight_layout()
plt.savefig("group_distributions_hist.png", dpi=150)
print("\nSaved group_distributions_hist.png")

# Box plots
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
df.boxplot(column="Row_CPA", by="Channel", ax=axes[0], rot=45)
axes[0].set_title("CPA by Channel")
df.boxplot(column="Row_Conversion_Rate", by="Channel", ax=axes[1], rot=45)
axes[1].set_title("Conversion Rate by Channel")
df.boxplot(column="Row_ROAS", by="Channel", ax=axes[2], rot=45)
axes[2].set_title("ROAS by Channel")

plt.suptitle("")
plt.tight_layout()
plt.savefig("group_distributions_box.png", dpi=150)
print("Saved group_distributions_box.png")