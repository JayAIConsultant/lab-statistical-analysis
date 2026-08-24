# Marketing Channel Statistical Analysis Lab

## Dataset
Shopping Mall Paid Search Campaign Dataset (Kaggle, marceaxl82) -- a real
2021 5-month Google Shopping Ads export, 190 rows (40 ad groups x up to 5
months), with Impressions, Clicks, Conversions, Cost, and Revenue per row.
Two other candidate datasets were evaluated and rejected before this one:
a media-spend dataset with no cost/conversion columns, and a "digital
marketing conversion" dataset explicitly tagged synthetic on Kaggle.

## Grouping Variable
The dataset's 40 ad groups were too granular (5 rows each) for meaningful
pairwise statistics, so a 6-channel grouping was derived from the ad group
naming convention: Device (Desktop/Mobile) x Match Type (1:1/Exact/Phrase).
Verified against all 190 rows with zero parsing failures. See
`data_exploration.py` for the derivation logic.

## Approach
1. Loaded and explored the raw CSV, derived the 6-channel grouping
   (`data_exploration.py` -> `marketing_data.csv`).
2. Calculated group-level metrics (CPA, ROAS, conversion rate, profit) via
   sum-then-divide aggregation, and row-level metrics for statistical
   testing (`calculate_metrics.py`, `distributions.py`).
3. Ran 15 pairwise Welch's t-tests on CPA (`ttests_comparison.py`) and 15
   pairwise Fisher's exact tests on conversion rate
   (`fisher_exact_comparisons.py`).
4. Applied Bonferroni and Benjamini-Hochberg (FDR) correction to both test
   families (`multiple_comparisons_correction.py`) -- all 5 apparent CPA
   findings were revealed as statistical noise; 14/15 conversion-rate
   findings survived even the strictest correction.
5. Ran power analysis via simulation to confirm the CPA null result
   reflects a real absence of effect, not insufficient data
   (`power_analysis.py`).
6. Synthesized bootstrap confidence intervals, a composite CPA/ROAS
   ranking, and a budget allocation table (`business_recommendations.py`),
   then wrote the executive memo and reflection.

## Key Finding
Every channel had ROAS below 1.0 (unprofitable) during the analyzed period.
CPA differences between channels do not survive multiple-comparisons
correction and should not drive budget reallocation. The Desktop-vs-Mobile
conversion rate gap (~2x) is real and statistically robust. Full details in
`executive_memo.md`.

## File Map
- `data/final_shop_6modata.csv` -- raw Kaggle download
- `marketing_data.csv` -- cleaned dataset with derived Channel grouping and row-level metrics
- `data_exploration.py` -- loads, cleans, derives Channel grouping
- `calculate_metrics.py` -- group-level metric aggregation + overview chart
- `distributions.py` -- row-level metrics + distribution histograms/boxplots
- `group_metrics_summary.csv`, `group_metrics_overview.png` -- Step 3 outputs
- `group_distributions_hist.png`, `group_distributions_box.png` -- Step 3 outputs
- `ttests_comparison.py` -- pairwise Welch's t-tests on CPA + Cohen's d
- `cpa_ttest_results.csv`, `metric_comparison_heatmap.png` -- Step 4 outputs
- `fisher_exact_comparisons.py` -- pairwise Fisher's exact tests on conversion rate
- `fisher_exact_results.csv`, `rate_comparison.png` -- Step 5 outputs
- `multiple_comparisons_correction.py` -- Bonferroni + FDR correction
- `correction_comparison_summary.csv`, `correction_comparison.png` -- Step 6 outputs
- `power_analysis.py` -- empirical power simulation
- `power_analysis_results.csv`, `power_analysis_cpa.png` -- Step 7 outputs
- `business_recommendations.py` -- bootstrap CIs, composite ranking, budget allocation
- `cpa_confidence_intervals.csv`, `budget_allocation.csv` -- Step 8 outputs
- `executive_memo.md` -- required executive memo with findings, recommendations, caveats
- `reflection.md` -- optional reflection questions

## How to Run
1. Activate the `bootcamp-env` conda environment.
2. Ensure `data/final_shop_6modata.csv` is present (downloaded manually from
   Kaggle -- see dataset link above).
3. Run scripts in order: `data_exploration.py` -> `calculate_metrics.py` ->
   `distributions.py` -> `ttests_comparison.py` ->
   `fisher_exact_comparisons.py` -> `multiple_comparisons_correction.py` ->
   `power_analysis.py` -> `business_recommendations.py`
