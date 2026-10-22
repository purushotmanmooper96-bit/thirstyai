# Original request: delivery and sign-off register

Reviewed 22 October 2026. This register describes the seven original tasks and final QA, rather than treating every future research idea as a promised feature. A completed evidence task can honestly report a gap. A prepared Desktop build is not a successful Desktop run. There is no guarantee of virality, stars, hiring or perfection.

## Task 1 — Company reporting

**Delivered:** three operators; 16 company metric records, including two missing numeric WUE values; company targets; hashes, timestamps and source locators; processed CSV, SQL table/view and plain-language case study. Periods, fleets, withdrawal/consumption, units, energy denominators and selected assurance are explicit. Missing WUE is not zero. Company values are not independently remeasured by this project.

Files: `research/sources.json`, `research/provenance.json`, `research/claims.json`, `research/company_targets.json`, `data/processed/company_water_reports.csv`, `sql/`, [case study](case_study_company_reporting.md).

Verified: source extraction reviews and semantic checks; three-view/five-query PostgreSQL/SQLite parity in release CI. Unverified: underlying company meters and omitted local details; no company ranking is justified. PowerShell: `python scripts/reproduce.py`.

## Task 2 — Location/stress overlay

**Delivered with a coarse geographic limit:** seven curated published location-water records; five have WRI state-level context; three regional scores; source licence and row locators retained. Exact facility/supply-basin matches remain **zero**. The UI and exports do not call a state proxy a facility risk rating. The small overlap is explicit, as requested. India groundwater is all-use context and a separate published WRI India analysis supplies the attributed data-centre connection.

Files: `scripts/overlay.py`, `data/processed/location_water.csv`, `data/processed/regional_water_stress.csv`, `data/processed/location_stress_overlay.csv`, [overlay method](location_overlay.md).

Verified: names, curated joins and boundary guards. Unverified: water supply basins, transfers and local causal effects. These need new source evidence, not a guessed coordinate. PowerShell: `python scripts/overlay.py; python scripts/reproduce.py`.

## Task 3 — Broader evidence

**Delivered as an evidence-status atlas:** ten areas each have a level, best source, caveat and missing evidence; gaps remain gaps. The NREL monthly-chart candidate records the difference between supply and consumption. A global withdrawal scenario candidate now has exact-byte provenance and is separated from headline evidence. It awaits genuine human locator/assumption review; no approval or reviewer identity is invented.

Files: [ten-topic status](evidence_status.md), [seasonal review](issue_resolutions/2_seasonal_source_search.md), [global scenario review](global_water_estimates.md), `research/reviews/global_projection_candidate.json`.

Verified: source opened and candidate metadata captured; registered source/claim checks remain intact. Unverified: independently observed global AI water, local seasonal peaks, chip allocation, discharge effects and the new candidate's human sign-off. A published projection is not a measured total. PowerShell: `python scripts/reproduce.py`.

## Task 4 — Cross-tool testing

**Partially signed off; preparation delivered.** PostgreSQL 16 has actually executed in GitHub CI and matched SQLite for all three views and five queries. Windows pgAdmin instructions, environment-variable verifier, Power BI model/DAX/theme/five-page instructions, Excel expected cases and a native Excel verifier exist. This follow-up adds a deterministic seven-table Power BI handoff, explicit null/type handling, M import query and regression checks.

Files: [PostgreSQL Windows guide](verify_postgres_windows.md), `scripts/verify_postgres.py`, [Power BI import](../bi/IMPORT_WINDOWS.md), [Power BI build](../bi/BUILD_WINDOWS.md), `bi/ThirstyAI_Data.m`, `scripts/build_bi_pack.py`, `tests/test_bi_pack.py`, [Excel checklist](excel_validation.md), `scripts/verify_excel.ps1`.

Verified: prepared data handoff, boundaries and source keys in automated tests. **Still required:** actual Excel Desktop recalculation; Power BI Desktop M/DAX/refresh/visual checks and saved report; the author's Windows PostgreSQL setup. The original instruction explicitly assigns PBIX authoring/screenshots to the author. No installed native applications are available in this execution environment. [Return actual evidence using this checklist](desktop_signoff.md); historical `limitations.md` stays unchanged until confirmation.

PowerShell:

```powershell
git pull --ff-only
python scripts/reproduce.py
Get-Content outputs/powerbi/manifest.json
.\scripts\verify_excel.ps1
```

Then follow the linked database and Power BI guides. An Excel self-test, CSV hash or generated M file does not count as native validation.

## Task 5 — Public explanation and README

**Delivered:** short first-use README plus a complete plain-language guide covering the problem, mechanism, boundaries, gaps, conditional futures, nine actor-specific actions with evidence limits, glossary, differentiation from Thirst, citation and Windows/macOS/Linux reproduction. The longer requested story is linked from the shorter README.

Files: [README](../README.md), [public guide](public_guide.md), [solutions](solutions_playbook.md), [Tamil introduction](translations/README.ta.md).

Verified: links, static content, no universal prompt factor, retained caveats. Unverified: reader comprehension/retention without real user research. PowerShell: `python scripts/check_repository.py`.

## Task 6 — Website

**Delivered:** canonical root URL and legacy redirect; static findings/sources/limits with no-JavaScript message; OG/Twitter card and custom image; fallback anchors; visible illustrative warnings and exports; keyboard/mobile regression coverage. Release Chrome and Lighthouse evidence is linked in [verification](verification_v021.md). Lighthouse is scoped lab evidence, not a full accessibility certificate.

Files: `dist/`, generated `docs/` site assets, `scripts/static_content.py`, `ci/browser-test.mjs`, `scripts/audit_site.py`.

Verified: release browser tests and live checks, local layout and lab scores. Unverified: physical devices, all assistive technologies and public-CDN field/load behavior. PowerShell: `npm ci --prefix ci; node ci/browser-test.mjs` with Chrome installed and `CHROME_PATH` set as in [current validation](validation_current.md).

## Task 7 — Repository and launch preparation

**Delivered:** topics, CI/licence/Python badges, changelog, release notes/commands, five contribution issues, published v0.2.1 release, product/growth audit, two built-in sharing mechanics and a seven-day distribution playbook. #1–#4 are completed; #5 remains open because native Excel evidence is missing. The launch drafts retain limitations. HN must be written personally under its rules, so the old AI-written draft has been removed.

Files: `CHANGELOG.md`, [release](RELEASE_v0.2.1.md), [launch drafts](launch_v02.md), [seven-day product/growth playbook](product_growth_audit_2026-10-22.md), [implementation map](implementation_2026-10-22.md).

Verified: release and merged CI; website social image. Unverified: GitHub repository-specific social-preview upload. Actual social posting was not required by the original draft/commands task and has not occurred. Publishing requires platform/account/content selection and current community rules; no engagement or reach is promised. PowerShell: `python scripts/check_repository.py`.

## Final QA

[The sceptical audit](audit.md) retains every headline's source, unit, period, geography and boundary, remaining weaknesses, a subjective six-part scorecard and five next fixes. Stale test counts, issue states and release instructions have been replaced with links to commit-specific validation records. No source candidate is promoted automatically by this cleanup.

## Follow-up local QA

`python scripts/reproduce.py` passed: 65 Python tests, 13 JavaScript tests, SQLite integrity and semantic checks, SQL/Python checks, 30 Python/JavaScript parity cases, notebook execution, syntax and documentation links. The seven added Power BI tests cover deterministic generation, missing values, source keys/boundaries, illustrative warnings, duplicate records, proxy scale and ten-topic coverage. No native application result is inferred.

## What prevents full sign-off

The remaining hard blockers are evidence from the author's native applications and human review where explicitly required. They cannot be completed by declaring success in this repository. Run [desktop_signoff.md](desktop_signoff.md), return the actual results and confirm them. Future basin/global measurement research remains explicitly scoped as missing evidence; producing fictional data would make the project worse, not complete it.
