import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def empirical_power_cpa(true_diff_pct, base_cpa, n_days, n_sim=1000, alpha=0.05):
    """Simulates n_sim experiments comparing two channels' CPA, where channel B
    truly differs from channel A by true_diff_pct. Returns the proportion of
    simulations where the t-test correctly detected the difference (power)."""
    rejections = 0
    std_a = base_cpa * 0.15
    cap_a = base_cpa * 0.5

    for _ in range(n_sim):
        sample_a = np.random.normal(base_cpa, std_a, n_days)
        sample_a = np.clip(sample_a, base_cpa - cap_a, base_cpa + cap_a)

        mean_b = base_cpa * (1 + true_diff_pct)
        std_b = mean_b * 0.15
        cap_b = mean_b * 0.5
        sample_b = np.random.normal(mean_b, std_b, n_days)
        sample_b = np.clip(sample_b, mean_b - cap_b, mean_b + cap_b)

        _, p = stats.ttest_ind(sample_a, sample_b, equal_var=False)
        if p < alpha:
            rejections += 1

    return rejections / n_sim


base_cpa = 7.5  # roughly the mid-range CPA across channels observed
effect_sizes = [0.05, 0.10, 0.15, 0.20]
sample_sizes = [30, 60, 90, 120, 180]

power_results = []
for effect in effect_sizes:
    for n in sample_sizes:
        power = empirical_power_cpa(effect, base_cpa, n, n_sim=500)
        power_results.append({"effect_size_pct": effect, "n_days": n, "power": power})
        print(f"Effect {effect*100:.0f}%, n={n}: power={power:.3f}")

power_df = pd.DataFrame(power_results)
power_df.to_csv("power_analysis_results.csv", index=False)

# Power curves
fig, ax = plt.subplots(figsize=(9, 6))
for effect in effect_sizes:
    subset = power_df[power_df["effect_size_pct"] == effect]
    ax.plot(subset["n_days"], subset["power"], marker="o", label=f"{effect*100:.0f}% difference")
ax.axhline(0.8, color="red", linestyle="--", label="80% power target")
ax.set_xlabel("Sample size (observations per group)")
ax.set_ylabel("Statistical Power")
ax.set_title("Power to Detect CPA Differences")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("power_analysis_cpa.png", dpi=150)
print("\nSaved power_analysis_cpa.png")

# Minimum sample size for 80% power, per effect size
print("\nMinimum sample size for 80% power:")
current_n = 30  # our actual per-channel row count is ~25-36
for effect in effect_sizes:
    subset = power_df[power_df["effect_size_pct"] == effect].sort_values("n_days")
    adequate = subset[subset["power"] >= 0.8]
    if len(adequate) > 0:
        min_n = adequate["n_days"].min()
        status = "SUFFICIENT" if current_n >= min_n else "INSUFFICIENT"
        print(f"  {effect*100:.0f}% difference: needs n={min_n} days ({status} — we have ~{current_n})")
    else:
        print(f"  {effect*100:.0f}% difference: 80% power not reached even at n=180 (need more)")