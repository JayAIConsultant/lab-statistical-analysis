# Executive Memo

**TO:** CMO
**FROM:** Jay, Marketing Analytics
**DATE:** August 24, 2026
**DATASET:** Shopping Mall Paid Search Campaign Dataset (Kaggle, real Google
Shopping Ads export, July-November 2021, 190 ad-group-months across 6
device x match-type channels)
**PERIOD ANALYZED:** 5 months (July-November 2021)

## Executive Summary
This analysis compared cost-efficiency (CPA) and conversion rate across 6
paid-search channel segments (Desktop/Mobile x 1:1/Exact/Phrase match type)
using t-tests, Fisher's exact tests, two multiple-comparisons correction
methods, and power analysis. The central finding: apparent CPA differences
between channels do not survive statistical correction and should NOT drive
budget reallocation, while the Desktop-vs-Mobile conversion rate gap is
extremely robust and is the one finding worth acting on. Critically, every
channel in this dataset operated at a loss (ROAS below 1.0, negative profit)
during the analyzed period -- a finding that matters more than any
channel-to-channel comparison.

## Key Findings

**Profitability (all channels, all months):** every one of the 6 channels
had ROAS below 1.0 (range: 0.72-0.93) and negative total profit during the
5-month period. This is a bigger issue than which channel is "best" -- the
whole campaign was unprofitable on a pure cost/revenue basis during this
window.

**CPA differences are not statistically robust.** 15 pairwise channel
comparisons were run on CPA; 5 appeared significant at the uncorrected
alpha=0.05 threshold, but 0 survived either Bonferroni or
Benjamini-Hochberg (FDR) correction. With 15 simultaneous comparisons, ~0.75
false positives were expected from chance alone -- the 5 apparent findings
are consistent with noise, not real channel differences. Power analysis
confirms this isn't a power problem: at the current sample size (~30
observations per channel), power to detect the 15-46% differences originally
observed was 94-99.6%, meaning if those differences were real, they very
likely would have survived correction. Their disappearance is evidence they
were not real, not evidence of insufficient data.

**Conversion rate differences are real and large.** 14 of 15 pairwise
comparisons remained significant even after the strict Bonferroni correction.
The pattern is coherent, not scattered: every Desktop channel converts at
roughly double the rate of every Mobile channel (Desktop: 16.3-18.6%,
Mobile: 6.4-8.0%). The only non-significant pair was Desktop-Exact vs.
Desktop-Phrase (p=0.30 even uncorrected) -- a genuine null result within the
same device. Given the enormous sample sizes involved (tens to hundreds of
thousands of clicks per channel), this result carries very high confidence
on sample-size grounds alone.

**Confidence intervals on CPA are wide for lower-volume channels.**
95% bootstrap CIs range from a tight $6.64-$7.17 (Desktop - 1:1, highest
volume) to $6.75-$10.86 (Mobile - Exact) and $7.42-$11.96 (Mobile - Phrase),
reflecting real uncertainty in the lower-volume segments that a point
estimate alone would hide.

## Recommendations

**Do not reallocate budget based on CPA differences between channels** -- the
statistical evidence does not support treating any channel as meaningfully
cheaper or more expensive than another on a corrected basis. A composite
CPA/ROAS ranking, while directionally informative, is built on differences
that were not statistically distinguishable from noise for most pairs and
should be treated as a soft prioritization signal, not a hard allocation
formula.

**Do treat Desktop's conversion-rate advantage as a real, actionable signal.**
This is the one finding in the analysis that is both statistically robust
(survives the strictest correction) and practically large (roughly 2x).
Recommend increasing testing/investment weight toward Desktop placements
relative to current spend share, while monitoring whether this shifts
overall campaign profitability.

**Address the profitability problem directly, independent of
channel-allocation questions.** Every channel is currently running at a
loss. Before optimizing *which* channel gets budget, the more urgent
question is whether the underlying offer, landing page, or bid strategy
needs to change, since reallocating a fixed loss-making budget across
loss-making channels does not solve the core problem.

## Statistical Caveats

- **Dataset scope:** single retailer, single 2021 paid-search account, 5
  months. Findings may not generalize to other retailers, channels
  (this analysis did not include organic, email, or social), or time
  periods (seasonality, e.g. November holiday shopping, is not separated
  out).
- **Correction method:** both Bonferroni (conservative) and
  Benjamini-Hochberg FDR (less conservative) were applied; they agreed on
  every CPA and conversion-rate result reported here, which strengthens
  confidence in the conclusions.
- **Statistical vs. practical significance:** the conversion-rate findings
  are significant partly *because* of very large sample sizes (hundreds of
  thousands of clicks) -- always confirm a finding is also practically
  meaningful, which in this case it is (a 2x rate difference clearly is).
- **Power analysis limitation:** power was estimated via simulation
  assuming normally-distributed CPA with a fixed 15% relative standard
  deviation; real CPA data showed heavier tails and outliers (max
  observed CPA values several multiples of the median), so actual power
  may differ somewhat from the simulated estimate.
- **Channel grouping:** the 6-channel grouping (Device x Match Type) was
  derived by parsing the dataset's own ad-group naming convention, not
  provided directly by the source -- verified against all 190 rows with
  zero parsing failures, but this is a derived variable, not a raw field.

## Next Steps
1. Investigate root cause of negative ROAS across all channels before any
   reallocation decision.
2. Run a properly powered, pre-registered test (not a retrospective
   comparison) specifically on the Desktop-vs-Mobile conversion gap to
   confirm it holds going forward, not just historically.
3. Extend data collection beyond match-type/device segments alone (e.g.,
   day-of-week, creative variant) if finer-grained budget decisions are
   needed, since current n per lower-volume segment (~25 rows) limits
   power to detect differences smaller than ~15%.
