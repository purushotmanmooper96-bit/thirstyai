# Issue 1: verify CORP04 against Google’s report

Result: value confirmed; reporting boundary and methodology locator corrected.

- Direct source: https://sustainability.google/files/google-2026-environmental-report.pdf
- Source: Google 2026 Environmental Report, PDF and printed p.96, Water use by data centers and offices, Data centers row, 2025 Water consumption column.
- Published value: **10,523 million gallons**, calendar 2025, global operational data-centre fleet. Confidence: High in source extraction; no independent measurement implied.
- Water methodology, pp.87–88: operations include owned and fully leased data centres; seawater and brackish water are excluded; consumption is withdrawal minus discharge; estimates can be used when metered/invoiced records are unavailable. This is not AI-only water or a universal cooling/prompt factor.
- The cell bears the selected-2025-metric check mark. The p.96 legend attributes that mark to third-party limited assurance. This review checked the legend and marked cell, not the full underlying assurance engagement or meter data.
- Assistant source-locator review: text plus rendered p.96. Author review is welcome. Machine-readable capture, UTC retrieval time, byte count, SHA-256 and reviewed fields: [issue_1_google_water.json](../../research/reviews/issue_1_google_water.json). The hash matches the existing GOOGLE26 source capture; no raw PDF is distributed.

Files: company CSV, corresponding claims, source locator, public README/case-study wording and generated exports. No numerical value was changed. Verification: `python scripts/reproduce.py`.
