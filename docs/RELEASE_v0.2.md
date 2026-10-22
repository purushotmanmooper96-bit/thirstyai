# ThirstyAI v0.2 — Evidence before headlines

AI's water footprint depends on place, time and accounting boundary. This release makes named company disclosures inspectable without turning unlike numbers into a league table.

New: three operators, 16 metric records (including two null WUE entries), seven curated location-water records, a deliberately coarse WRI state-context overlay, ten-topic evidence status, public story, static HTML and canonical URL, custom social card, clearer hypothetical exports, PostgreSQL verifier and desktop build/validation guides.

Verified: offline rebuild, semantic guards and calculation parity; Windows/Linux CI and actual PostgreSQL 16 comparison. See [validation record](validation_v02.md) and [site QA](site_qa.md) for run IDs and scoped measurements.

Limits: company self-reports are not independently remeasured. Some metrics have limited external assurance. Years, units and fleets differ. The overlay has five state matches and zero verified exact facility/basin joins. No global AI water total, universal water-per-prompt claim, PBIX or confirmed Microsoft Excel Desktop recalculation. The workbook is an older snapshot; scenario inputs are hypothetical, not observations or achieved savings.

[Live atlas](https://purushotmanmooper96-bit.github.io/thirstyai/) · [Source register](../research/sources.json) · [Case study](case_study_company_reporting.md) · [Audit](audit.md)

## PowerShell: tag and publish

Run from the public GitHub checkout after pulling the final reviewed commit. The user requested notes and commands; actual tag/release creation remains a maintainer step. Install/authenticate the official GitHub CLI for `gh`.

```powershell
git pull --ff-only origin main
python scripts/reproduce.py
git status --short
# Inspect expected generated changes before tagging.
git tag -a v0.2.0 -m "ThirstyAI v0.2: evidence before headlines"
git push origin v0.2.0
gh release create v0.2.0 --repo purushotmanmooper96-bit/thirstyai --verify-tag --title "ThirstyAI v0.2 — Evidence before headlines" --notes-file docs/RELEASE_v0.2.md
```

Tags must identify the checked commit; do not reuse an existing tag by force.
