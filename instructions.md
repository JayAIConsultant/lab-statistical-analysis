# In God we trust, everyone else bring the data

> **How you'll submit this lab**
>
> This repo is your lab. Fork it, do the work described below in your fork, then open a pull
> request back into this repository. An AI reviewer will check your PR against `rubric.md` and
> leave feedback directly on the PR. See `README.md` for the full workflow.

**Scenario**  
You're a marketing analyst at a growing e-commerce company. The CMO has asked you to analyze marketing channel performance and recommend how to allocate the $500K monthly marketing budget across 7 channels. Your analysis must be statistically rigorous to avoid costly mistakes—false positives could lead to shifting budget to underperforming channels.

**Learning Objectives**
- [ ] Find and evaluate real marketing/advertising datasets from Kaggle or Hugging Face
- [ ] Load and explore real-world marketing channel performance data
- [ ] Calculate key marketing metrics (CPA, ROAS, conversion rates) across channels or campaigns
- [ ] Apply appropriate statistical tests (t-tests, Fisher's exact test) to compare performance
- [ ] Calculate effect sizes (Cohen's d) to assess practical significance of differences
- [ ] Apply multiple comparisons correction (Bonferroni, Benjamini-Hochberg) to control false discovery rates
- [ ] Perform power analysis to determine adequate sample sizes for future tests
- [ ] Synthesize statistical findings into actionable business recommendations with proper caveats

**Estimated Time:** 180-240 minutes (3-4 hours)

**Prerequisites:**
- [ ] Understanding of statistical analysis concepts from the statistical analysis notebook
- [ ] Familiarity with Python (numpy, pandas, scipy, matplotlib)
- [ ] Basic understanding of marketing metrics (CPA, ROAS, conversion rate)
- [ ] Knowledge of hypothesis testing and p-values

---

## Introduction

This lab applies statistical analysis to real-world marketing data. You will:
1. **Discover** and select a real marketing/advertising dataset from Kaggle or Hugging Face
2. **Explore** the dataset to understand its structure and identify comparable groups (channels, campaigns, etc.)
3. **Compare** groups using appropriate statistical tests
4. **Correct** for multiple comparisons to avoid false discoveries
5. **Analyze** statistical power to assess data adequacy
6. **Recommend** actionable insights with statistical backing and proper caveats

**Why this matters:**
- Real datasets provide authentic patterns and challenges
- Without statistical rigor, you risk false positives that lead to poor decisions
- Multiple comparisons correction is essential when testing many groups
- Power analysis helps determine if you have enough data to make reliable conclusions
- Professional analysis requires translating statistics to business language

**Success criteria:**
- [ ] Generated and explored marketing channel dataset
- [ ] Performed pairwise comparisons with appropriate statistical tests
- [ ] Applied multiple comparisons correction correctly
- [ ] Calculated power and sample size requirements
- [ ] Generated business recommendations with statistical backing
- [ ] Created executive memo with proper hedging and caveats
- [ ] All code runs without errors

---

## Part 1: Dataset Discovery & Exploration (45-60 min)

### Step 1: Find and Select a Dataset (20-30 min)

**Objective:** Find a real marketing, advertising, or e-commerce dataset from Kaggle or Hugging Face that allows for multi-group comparison.

**What to do:**

1. **Search for suitable datasets (limit: 30 minutes research):**
   - Go to **Kaggle** (https://www.kaggle.com/datasets) or **Hugging Face** (https://huggingface.co/datasets)
   - Search for keywords like:
     - "marketing channels"
     - "advertising campaigns"
     - "e-commerce conversion"
     - "A/B testing"
     - "marketing attribution"
     - "ad spend"
     - "campaign performance"
   - Look for datasets that have:
     - Multiple groups/channels/campaigns to compare (at least 3-5 groups)
     - Performance metrics (conversions, clicks, revenue, cost, etc.)
     - Sufficient sample size (hundreds to thousands of observations per group)
     - Time series or aggregated data suitable for statistical analysis

2. **Evaluate potential datasets:**
   - Check dataset description and documentation
   - Review data preview/sample
   - Verify it has the necessary columns for comparison
   - Ensure data quality (no excessive missing values, reasonable value ranges)
   - Check dataset size (should be manageable to load and process)

3. **Select your dataset:**
   - Choose one dataset that interests you and meets the requirements
   - Document your choice: dataset name, source (Kaggle/Hugging Face), URL, why you chose it
   - Note: Popular options include:
     - Kaggle: "Marketing Campaign Performance", "E-commerce A/B Testing", "Advertising Campaign Data"
     - Hugging Face: Search for marketing/advertising related datasets
   - **Time limit: Don't spend more than 30 minutes researching. Pick one and proceed.**

### Step 2: Load and Explore Your Dataset (25-30 min)

**Objective:** Load your chosen dataset and understand its structure.

**What to do:**

1. **Set up your environment:**
   - Import necessary libraries: `numpy`, `pandas`, `matplotlib`, `seaborn`, `scipy.stats`
   - Import specific functions: `fisher_exact` and `false_discovery_control` from `scipy.stats`
   - **Tip:** `false_discovery_control` requires **SciPy 1.11+**. If your environment is older, upgrade with `pip install -U scipy` or use manual Benjamini–Hochberg adjustment per the SciPy docs.
   - If using Hugging Face, install and import: `datasets` library
   - Optionally set a plotting style

2. **Load the dataset:**
   - For Kaggle: Download and load the CSV/Excel file using `pd.read_csv()` or `pd.read_excel()`
   - For Hugging Face: Use `datasets.load_dataset()` to load the dataset
   - Convert to pandas DataFrame if needed
   - Print basic info: shape, columns, data types, first few rows

3. **Explore the data structure:**
   - Identify the grouping variable (what defines your "channels" or groups to compare):
     - Could be: campaign names, channel types, ad groups, landing pages, countries, etc.
     - Should have at least 3-5 distinct groups
   - Identify performance metrics available:
     - Conversions, clicks, impressions, cost, revenue, conversion rate, etc.
     - Note which metrics are available and which might need to be calculated
   - Check data quality:
     - Missing values
     - Data types (ensure numeric columns are numeric)
     - Outliers or unusual values
     - Date/time columns if present

4. **Prepare the data for analysis:**
   - Clean the data: handle missing values, fix data types, remove obvious errors
   - If needed, aggregate data to a consistent level (e.g., daily, weekly, or by group)
   - Create or calculate any missing metrics:
     - If you have clicks and conversions: calculate conversion rate
     - If you have cost and conversions: calculate CPA
     - If you have revenue and cost: calculate ROAS
     - If you have impressions and clicks: calculate CTR
   - Ensure you have a grouping variable and at least one continuous metric (like CPA, ROAS, conversion rate) and/or binary outcomes (conversions) for statistical testing

5. **Save your prepared dataset:**
   - Save the cleaned/prepared dataset as `marketing_data.csv` or similar
   - Document what transformations you made
   - Print summary statistics: number of groups, sample sizes per group, date range (if applicable)

**Deliverable:** 
- Documentation of your dataset choice (name, source, URL, why you chose it)
- Loaded and explored dataset
- Summary of data structure: groups identified, metrics available, sample sizes
- Cleaned dataset saved to CSV

---

### Step 2: Calculate Key Marketing Metrics (15-20 min)

**Objective:** Calculate and explore key performance metrics for each channel.

**What to do:**

1. **Calculate aggregate metrics by channel:**
   - Group the data by channel and sum: impressions, clicks, conversions, cost, revenue
   - Calculate the following metrics for each channel:
     - CTR (Click-Through Rate) = clicks / impressions
     - Conversion Rate = conversions / clicks
     - CPA (Cost Per Acquisition) = cost / conversions
     - ROAS (Return on Ad Spend) = revenue / cost
     - Profit = revenue - cost
     - Profit Margin = profit / revenue
   - Handle infinite values (channels with zero cost will have infinite ROAS) by replacing with NaN
   - Display a summary table with all metrics rounded to 2 decimal places

2. **Visualize key metrics:**
   - Create subplot figures (adjust grid size based on available metrics)
   - Plot horizontal bar charts for available metrics:
     - CPA by group (if cost and conversions available)
     - ROAS by group (if revenue and cost available)
     - Conversion rate by group (if conversions and clicks available)
     - Total conversions by group
     - Total cost by group (if available)
     - Profit by group (if revenue and cost available, include vertical line at 0)
   - Add appropriate labels, titles, and formatting
   - Save as `group_metrics_overview.png`

3. **Examine distributions:**
   - If your data has time granularity (daily, weekly), calculate per-period metrics:
     - Daily/weekly CPA, conversion rate, ROAS (if applicable)
   - Handle infinite/NaN values appropriately
   - Create visualization showing distributions:
     - Histogram overlay of metric distributions by group (use transparency for multiple groups)
     - Box plots of key metrics by group
   - Add legends, labels, and rotate x-axis labels if needed
   - Save as `group_distributions.png`

**Deliverable:** 
- Group summary table with key metrics
- Visualization of group performance
- Distribution plots showing variability

**Key insights to note:**
- Which groups perform best on each metric?
- Which groups show the most variability in performance?
- Are there any obvious outliers?
- What patterns do you observe?

---

## Part 2: Pairwise Group Comparisons (60-75 min)

### Step 4: Compare Groups Using t-tests (30-40 min)

**Objective:** Use t-tests to compare continuous metrics between groups.

**What to do:**

1. **Compare continuous metrics between groups:**
   - Identify which continuous metrics you can compare (CPA, ROAS, conversion rate, etc.)
   - For each metric:
     - Prepare the data: remove rows with NaN or infinite values, filter out invalid values
     - Get unique groups from the cleaned data
     - For each unique pair of groups (avoid duplicates):
       - Extract metric values for both groups
       - Perform an independent t-test using `scipy.stats.ttest_ind()`
       - Calculate means and the difference (group B - group A)
       - Calculate percentage difference: `(difference / mean_A) × 100`
       - Calculate Cohen's d for effect size:
         - Pooled standard deviation = `sqrt((var_A + var_B) / 2)`
         - Cohen's d = `difference / pooled_std`
       - Interpret effect size: < 0.2 = negligible, < 0.5 = small, < 0.8 = medium, ≥ 0.8 = large
       - Store results: group names, means, difference, percentage difference, t-statistic, p-value, Cohen's d, effect size interpretation, significance flag (p < 0.05)
       - Print formatted results for each comparison
     - Convert results to a DataFrame for easier analysis
     - Print summary: total comparisons made, number significant at α=0.05

2. **Visualize comparison results:**
   - Create a heatmap of p-values for your primary metric:
     - Build a square matrix (groups × groups)
     - Fill matrix with p-values from your comparisons (symmetric matrix)
     - Set diagonal to 1.0 (group compared to itself)
     - Use a colormap (e.g., 'RdYlGn_r') where red = significant, green = not significant
     - Add text annotations showing p-values
     - Include colorbar with label
     - Save as `metric_comparison_heatmap.png`

**Deliverable:** 
- Comparison results table with p-values and effect sizes
- Heatmap visualization of p-values
- Summary of which channels are significantly different

---

### Step 5: Compare Binary Outcomes Using Fisher's Exact Test (30-35 min)

**Objective:** Use Fisher's exact test to compare binary outcomes (conversions, clicks, etc.) between groups.

**What to do:**

1. **Compare binary outcomes using Fisher's exact test:**
   - Identify binary outcomes in your data (conversions, clicks, purchases, etc.)
   - If you have conversions and total attempts (clicks, visits, etc.):
     - Aggregate by group: sum conversions and total attempts
     - Calculate non-conversions = total attempts - conversions for each group
     - Display a summary table showing: group, conversions, total attempts, non-conversions
   - For each unique pair of groups:
     - Create a 2×2 contingency table:
       ```
       [[conversions_A, non_conversions_A],
        [conversions_B, non_conversions_B]]
       ```
     - Perform Fisher's exact test using `scipy.stats.fisher_exact()` with `alternative='two-sided'`
     - Calculate rates for both groups (e.g., conversion rate = conversions / total attempts)
     - Calculate difference and percentage difference
     - Store results: group names, conversion counts, total attempt counts, rates, difference, odds ratio, p-value, significance flag
     - Print formatted results for each comparison
   - Convert results to a DataFrame
   - Print summary: total comparisons, number significant at α=0.05

2. **Visualize rate comparisons:**
   - Create a horizontal bar chart comparing rates across all groups
   - Sort groups by count (or rate) for better visualization
   - Add value labels on bars showing the percentage
   - Include appropriate labels and title
   - Save as `rate_comparison.png`

**Deliverable:**
- Fisher's exact test results for all channel pairs
- Conversion rate comparison visualization
- Summary of significant differences

**Key questions:**
- Which channels have significantly different conversion rates?
- Are the differences practically significant (large enough to matter)?
- How do Fisher's exact test results compare to t-test results on conversion rates?

---

## Part 3: Multiple Comparisons Correction (45-60 min)

### Step 6: Apply Multiple Comparisons Correction (45-60 min)

**Objective:** Apply Bonferroni and Benjamini-Hochberg corrections to control false discovery rates.

**What to do:**

1. **Understand the multiple comparisons problem:**
   - Count the total number of comparisons made (CPA comparisons + conversion rate comparisons)
   - Calculate expected false positives: `total_comparisons × 0.05`
   - Print a summary explaining that with α=0.05, we expect false positives by chance alone
   - Explain that some "significant" results are likely due to random variation

2. **Apply Bonferroni correction:**
   - Set α = 0.05
   - Calculate Bonferroni-adjusted α for each set of comparisons:
     - `alpha_bonferroni = alpha / number_of_comparisons`
   - Apply to CPA comparisons: create a new column `significant_bonferroni` where `p_value < alpha_bonferroni_cpa`
   - Apply to conversion rate comparisons similarly
   - Print how many comparisons remain significant after Bonferroni correction
   - Display which specific comparisons remain significant (if any)

3. **Apply Benjamini-Hochberg FDR correction:**
   - Use `scipy.stats.false_discovery_control()` with `method='bh'` on the p-values
   - Apply to both CPA and conversion rate p-value arrays
   - Create new columns: `p_value_fdr` (adjusted p-values) and `significant_fdr` (adjusted < α)
   - Print how many comparisons remain significant after FDR correction
   - Display which specific comparisons remain significant (if any)
   - Note: FDR controls the expected proportion of false discoveries, not the probability of any false positive. It's less conservative than Bonferroni.

4. **Compare correction methods:**
   - Create a summary table comparing:
     - Uncorrected (α=0.05): number of significant comparisons
     - Bonferroni: number of significant comparisons
     - FDR (Benjamini-Hochberg): number of significant comparisons
   - Do this for both CPA and conversion rate comparisons
   - Create a bar chart visualization showing the effect of each correction method
   - Save as `correction_comparison.png`

**Deliverable:**
- Comparison of significant results before and after correction
- Summary table showing effect of each correction method
- Visualization of correction impact

**Key insights:**
- How many "significant" results were false positives?
- Which correction method is more appropriate for this scenario?
- What are the practical implications for budget allocation?

---

## Part 4: Power Analysis & Sample Size Planning (30-45 min)

### Step 7: Perform Power Analysis (30-45 min)

**Objective:** Calculate statistical power and determine adequate sample sizes for future tests.

**What to do:**

1. **Calculate empirical power for detecting CPA differences:**
   - Create a function `empirical_power_cpa(true_diff_pct, base_cpa, n_days, n_sim=1000, alpha=0.05)`:
     - Simulate `n_sim` experiments
     - For each simulation:
       - Generate `n_days` of CPA data for channel A: normal distribution with mean=`base_cpa`, std=`base_cpa × 0.15`, cap at 50% of base
       - Generate `n_days` of CPA data for channel B: normal distribution with mean=`base_cpa × (1 + true_diff_pct)`, same std and cap
       - Perform t-test between the two samples
       - Count if p-value < alpha (rejection of null hypothesis)
     - Return proportion of simulations that rejected H0 (this is the power)
   - Calculate power for different effect sizes (5%, 10%, 15%, 20% differences) and sample sizes (30, 60, 90, 120, 180 days)
   - Store results in a DataFrame with columns: effect_size_pct, n_days, power
   - Visualize power curves:
     - Plot power vs. sample size for each effect size (different lines)
     - Add a horizontal line at 80% power (standard target)
     - Include legend, labels, title, grid
     - Save as `power_analysis_cpa.png`
   - Print a formatted table showing power for each effect size and sample size combination

2. **Determine minimum sample size for desired power:**
   - Set target power = 0.80 (80%)
   - For each effect size:
     - Find the minimum number of days needed to achieve 80% power
     - Check if current data (90 days) is sufficient
     - Print a table showing: effect size, minimum days needed, current data status (sufficient/insufficient)

3. **Assess current data adequacy:**
   - For each channel pair that showed significant difference after FDR correction:
     - Calculate the observed difference as a percentage
     - Use the smaller mean as baseline
     - Calculate power to detect this observed difference with 90 days of data
     - If power < 0.8, estimate how many days would be needed for 80% power
     - Print assessment for each significant pair

**Deliverable:**
- Power curves for different effect sizes
- Minimum sample size recommendations
- Assessment of current data adequacy

**Key questions:**
- Do we have enough data to detect meaningful differences?
- What effect sizes can we reliably detect with 90 days of data?
- How many more days would we need to achieve 80% power?

---

## Part 5: Business Recommendations (30-45 min)

### Step 8: Synthesize Findings and Create Recommendations (30-45 min)

**Objective:** Translate statistical findings into actionable business recommendations with proper caveats.

**What to do:**

1. **Create summary of statistically significant findings:**
   - Compile all significant findings using FDR-corrected results
   - For CPA differences: identify which channel has lower CPA, calculate absolute difference, include adjusted p-value and Cohen's d
   - For conversion rate differences: identify which channel has higher rate, calculate absolute difference, include adjusted p-value
   - Print a formatted summary of all significant findings

2. **Calculate confidence intervals for key metrics:**
   - Create a bootstrap function `bootstrap_ci(data, n_bootstrap=1000, ci_level=0.95)`:
     - Resample the data with replacement `n_bootstrap` times
     - Calculate the mean for each bootstrap sample
     - Find the (α/2) and (1-α/2) percentiles of bootstrap means
     - Return lower and upper bounds
   - For each channel, calculate 95% confidence interval for CPA
   - Display a table showing: channel, mean CPA, 95% CI lower, 95% CI upper

3. **Create actionable recommendations:**
   - Rank groups by creating a composite score (if you have multiple metrics):
     - Rank groups by each available metric (invert ranks where lower is better)
     - Weight metrics appropriately (e.g., if CPA and ROAS available: 50% each)
     - Composite score = weighted sum of ranks
     - Sort groups by composite score (descending)
   - If applicable to your dataset, create resource allocation recommendations:
     - Allocate resources proportionally to composite score
     - Apply reasonable constraints (minimum/maximum per group)
     - Display allocation table showing: group, allocation amount, allocation percentage
   - If not applicable, create prioritization recommendations:
     - Which groups should receive more focus/investment?
     - Which groups should be deprioritized?
     - What actions should be taken based on the statistical findings?

4. **Write executive memo:**
   - Create a professional memo template with the following sections:
     - Header: Title, Date, Analyst name, Dataset used, Period analyzed (if applicable)
     - Executive Summary: Brief overview of findings
     - Key Findings:
       - Top performing groups (based on your metrics)
       - Statistically significant differences found
       - Data adequacy assessment (power analysis results)
     - Recommendations:
       - Resource allocation or prioritization (if applicable)
       - Strategic actions based on findings
     - Statistical Caveats:
       - Dataset limitations and source
       - Multiple comparisons correction applied
       - Confidence intervals
       - External factors that may affect results
       - Statistical vs. practical significance
       - Power analysis limitations
     - Next Steps: Action items
   - Include power analysis results in the data adequacy section
   - Save memo as `executive_memo.md`

**Deliverable:**
- Summary of statistically significant findings
- Budget allocation recommendations with justification
- Executive memo with proper statistical caveats
- Confidence intervals for key metrics

---

## Deliverables

### Submission hygiene

- **Filenames:** Use clear, descriptive names (avoid vague names such as `lab.ipynb`, `final_v2.py`, or `untitled.md`).
- **Scope:** Your **GitHub** repository must contain **only materials for this lab**—no unrelated projects, dumps, or personal files.
- **README:** Include a `README.md` that briefly explains what each main file or folder is for (a short map of your file structure).

**GitHub only:** Submit the URL to a **GitHub repository** that contains everything for this lab (Markdown, code, exports, images, decks). Do **not** submit a standalone Google Doc, Notion page, or cloud-only link as your primary deliverable—put sources or exports (for example `.md`, `.pdf`, `.pptx`, screenshots) **in the repository**.

Submit the following items:

1. **Data Exploration (Part 1)**
   - Dataset documentation (name, source, URL, why you chose it)
   - Loaded and cleaned dataset (CSV file)
   - Data exploration notebook/code
   - Group performance summary table
   - Visualization of key metrics and distributions
   - Saved as: `data_exploration.py` or `data_exploration.ipynb`

2. **Statistical Analysis (Parts 2-3)**
   - Pairwise comparison results (CPA and conversion rates)
   - Multiple comparisons correction results
   - Summary tables showing effect of corrections
   - Visualizations (heatmaps, comparison charts)
   - Saved as: `statistical_analysis.py` or `statistical_analysis.ipynb`

3. **Power Analysis (Part 4)**
   - Power curves for different effect sizes
   - Minimum sample size recommendations
   - Current data adequacy assessment
   - Saved as: `power_analysis.py` or included in main analysis notebook

4. **Business Recommendations (Part 5)**
   - Executive memo with findings and recommendations
   - Budget allocation table
   - Confidence intervals for key metrics
   - Saved as: `executive_memo.md`

5. **Reflection (Optional but Recommended)**
   - What surprised you about the results?
   - How did multiple comparisons correction change your conclusions?
   - What are the limitations of this analysis?
   - How would you communicate these findings to non-technical stakeholders?
   - Saved as: `reflection.md`

**Submission Format:**
- Create a folder: `lab_statistical_analysis_[your_name]`
- Include all deliverables above
- Add a `README.md` with:
  - How to run your code (if applicable)
  - A **file map** (what each main file or folder is for)
  - Any setup assumptions (keep narrative overview and key findings in **`executive_memo.md`** / notebooks—**not** a long write-up in `README.md`)

---

## Success Criteria

Your lab is complete when:
- [ ] You've found and selected a real dataset from Kaggle or Hugging Face
- [ ] You've loaded and explored your dataset, identifying groups and metrics
- [ ] You've performed pairwise comparisons with appropriate statistical tests (t-tests, Fisher's exact)
- [ ] You've calculated effect sizes (Cohen's d) for all comparisons
- [ ] You've applied multiple comparisons correction (Bonferroni and FDR)
- [ ] You've performed power analysis and determined sample size requirements
- [ ] You've created actionable recommendations with statistical backing
- [ ] You've written an executive memo with proper hedging and caveats
- [ ] All code runs without errors
- [ ] All deliverables are submitted in the required format

---

## Tips & Troubleshooting

**Common Issues:**

1. **Infinite or NaN values in CPA/ROAS calculations**
   - Some channels (like SEO) may have zero cost, leading to division by zero
   - Solution: Filter out or handle zero-cost channels separately
   - Use `replace([np.inf, -np.inf], np.nan)` to clean data

2. **Very small p-values showing as 0.0000**
   - This is normal for very significant results
   - Use scientific notation or round to more decimal places for display
   - Example: `f"{p_value:.6e}"` for scientific notation

3. **Power analysis taking too long**
   - Reduce `n_sim` parameter (default 1000) to 500 or 300 for faster results
   - Power estimates will be slightly less precise but still useful

4. **No significant results after correction**
   - This is actually a good thing! It means you're being appropriately conservative
   - Consider:
     - Increasing sample size (more days of data)
     - Focusing on larger effect sizes
     - Using less conservative correction (FDR instead of Bonferroni)

5. **Confidence intervals seem very wide**
   - This reflects real uncertainty in your estimates
   - Wider CIs indicate you need more data for precise estimates
   - Report this as a limitation in your memo

6. **Effect sizes seem small but p-values are significant**
   - This can happen with large sample sizes
   - Consider both statistical and practical significance
   - A $1 difference in CPA might be statistically significant but not practically meaningful
   - Report both in your recommendations

**Best Practices:**

- Always check data quality before analysis (missing values, outliers, distributions)
- Use appropriate statistical tests for your data type (t-test for continuous, Fisher's for binary)
- Always apply multiple comparisons correction when testing many hypotheses
- Report confidence intervals, not just point estimates
- Consider both statistical and practical significance
- Include proper caveats in business recommendations
- Visualize your results - charts help communicate findings

**Getting Help:**

- Review the statistical analysis notebook for concepts and examples
- Check scipy.stats documentation for test functions
- Consult with instructor if you're unsure about test selection
- Test your code incrementally - don't wait until the end to run everything

---

## Reference Materials

**Statistical Concepts:**
- Statistical Analysis Notebook: `03_statistical_analysis.ipynb`
- Scipy Stats Documentation: https://docs.scipy.org/doc/scipy/reference/stats.html

**Marketing Metrics:**
- CPA (Cost Per Acquisition) = Total Cost / Total Conversions
- ROAS (Return on Ad Spend) = Revenue / Cost
- Conversion Rate = Conversions / Clicks
- CTR (Click-Through Rate) = Clicks / Impressions

**Multiple Comparisons:**
- Bonferroni Correction: Divide α by number of tests
- Benjamini-Hochberg FDR: Controls false discovery rate (less conservative)
- Use FDR when testing many hypotheses (better power)

**Power Analysis:**
- Power = Probability of detecting a real difference when it exists
- Target: 80% power is standard
- Larger effect sizes require smaller sample sizes
- More data = higher power to detect smaller differences

---

*Good luck with your analysis! Remember: statistical rigor prevents costly mistakes in budget allocation.*
