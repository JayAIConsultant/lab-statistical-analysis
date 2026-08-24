# Reflection

## What surprised you about the results?
The starkest surprise wasn't a channel comparison at all -- it was that
every single channel had ROAS below 1.0 and negative profit across the
entire 5-month period. It's easy to get pulled into "which channel is best"
framing and miss that the more urgent finding is "none of them are
profitable." The second surprise was how completely the CPA findings
collapsed under correction: 5 out of 15 comparisons looked meaningfully
significant before correction, and all 5 vanished after. Seeing that happen
in real data, rather than as an abstract warning in the lesson, made the
multiple-comparisons problem concrete in a way the concept alone hadn't.

## How did multiple comparisons correction change your conclusions?
It completely reversed the CPA conclusion. Before correction, I would have
told the CMO that several specific channel pairs had meaningfully different
CPA and recommended shifting budget accordingly -- a real, costly mistake
per the lab's own framing. After correction, the honest conclusion is "we
cannot statistically distinguish CPA between channels with this data,"
which is a very different, much more conservative message. The conversion
rate conclusion barely moved (14/15 significant before, 14/15 after) because
the effect was large and the sample sizes were enormous -- correction matters
most exactly where the underlying signal is weak, which is precisely where
it's most tempting to over-interpret a result.

## What are the limitations of this analysis?
Single retailer, single account, one paid-search channel type (Shopping
ads only -- no organic, email, or social for comparison), and a 5-month
window that includes November, which likely has real seasonal effects not
separated out from channel effects. The channel grouping itself (Device x
Match Type) was derived by parsing ad-group names rather than being a
native field in the data, so it depends on the naming convention holding
consistently, which we verified but is still a derived category. Power
analysis used a simplified simulation model that may not perfectly capture
the actual variance structure (real CPA data showed heavier-tailed
outliers than a normal distribution would produce).

## How would you communicate these findings to non-technical stakeholders?
Lead with the two things that matter for a decision, not the statistics
that produced them: "every channel is currently losing money, and that's
the real problem to solve before deciding where to shift budget" and
"Desktop converts about twice as well as Mobile, and that difference is
solid enough to act on." Leave the p-values and correction methods in an
appendix or available on request, but don't lead with them -- a CMO needs
the business implication first, with the rigor available as backup for
"how do you know," not as the headline. This mirrors the discipline from
the should-cost agent's report generator: state confirmed conclusions
plainly, keep the uncertainty and methodology honest but out of the way of
the main message.
