# v0.2.1 verification

Published 22 October 2026. Release tag: `v0.2.1`, commit `e415ebe556592d02fe3eb4527c8276257d1a41c5`.

- [Main CI](https://github.com/purushotmanmooper96-bit/thirstyai/actions/runs/39786753268): Windows, Linux, PostgreSQL and browser/Lighthouse jobs all passed.
- [PR audit run](https://github.com/purushotmanmooper96-bit/thirstyai/actions/runs/39786493031): 58 Python tests, 13 JavaScript tests and seven Chrome interaction groups passed. The artifact includes PNG result output and screenshots.
- [Pages deployment](https://github.com/purushotmanmooper96-bit/thirstyai/actions/runs/39786750938): successful.
- Lighthouse 12.8.2 against CI-served files: mobile performance 97; accessibility, best practices and SEO 100. Desktop 100 in all four categories. These are scoped lab measurements, not public-CDN field performance or WCAG certification.
- Browser groups: guided challenge; invalid/corrected input gating; JSON/PNG download; clipboard-link round trip/reset; company filters/conversion/all locations; desktop/mobile keyboard and overflow; evidence 503 fallback/retry.
- Repeated build output is byte-stable. Failed refresh preserves reviewed snapshots; promotion rejects a mismatched reviewed hash.
- Live connected Chrome: v0.2.1 heading/entry points visible; blank workload hides results and disables share/card/JSON export; valid workload restores the result. The definition challenge reveals its explanation and enables its card.

[Current website screenshot](../outputs/website-v021.png). The published release links its immutable source snapshot. No social posts have been sent. Excel Desktop and Power BI Desktop remain unconfirmed; issue #5 is open awaiting native evidence and author confirmation. See [current validation](validation_current.md).

PowerShell after pulling:

```powershell
git pull --ff-only
python scripts/reproduce.py
```
