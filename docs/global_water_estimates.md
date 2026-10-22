# Is there a global AI water number?

There are published modeled scenarios. ThirstyAI has no measured global AI water inventory. A future scenario must not be presented as today's observed consumption.

## Source candidate, awaiting human locator review

[Li, Yang, Islam and Ren, arXiv:2304.03271v5](https://arxiv.org/html/2304.03271v5), revised 26 March 2025: Abstract and Section 1, paragraphs beginning “AI represents” and “Even considering”, including the scope-2 footnote.

| Field | Meaning |
|---|---|
| Published range | 4.2–6.6 billion cubic metres per year |
| Target year / geography | 2027 / global AI demand |
| Quantity / boundary | Water **withdrawal**; operational on-site scope 1 plus location-based electricity scope 2; excludes manufacturing |
| Evidence class | Published conditional projection; not a measured inventory |
| Confidence in applicability | Low; assumed demand and water factors; not a statistical confidence interval |
| Review state | Source opened and assistant-reviewed; **human review pending**, excluded from headline claims and the calculator |

The paper links its scenario to assumed electricity demand and water intensities. Its withdrawal and consumption estimates are separate. Do not add the range to company totals, apply it per prompt or extend it to 2035. The arXiv version uses a non-exclusive distribution licence; this repo stores attribution and metadata, not the paper.

## Why this does not close the research gap

A scenario is useful for asking which assumptions matter. It does not supply an observed workload inventory, current location shares, local water sources or basin-level effects. Nor does a range tell us the probability of an outcome. Converting a global withdrawal scenario into local scarcity or harm would require new evidence.

The [candidate capture](../research/reviews/global_projection_candidate.json) records the exact URL, UTC retrieval time, byte count, SHA-256, boundary and review state. Raw downloaded HTML remains ignored under `data/raw/`. The captured bytes were checked at the stated sections. This is not an independent human review. A maintainer must inspect the exact source and record that review before promoting any figure through the [review workflow](source_refresh.md). Do not change `human_reviewed` merely to make a check pass.

## A useful next contribution

Review the source's global demand assumptions and the transfer of water intensities between regions. Explain whether the scenario remains useful for its target year; document disagreement rather than calling it a consensus forecast. Keep any new literature estimate separate from the site's illustrative consumption scenarios and reported company evidence.
