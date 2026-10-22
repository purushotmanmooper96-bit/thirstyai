# Contributing

Start with a bug, data-correction or new-source issue. Include source URL and locator, observation period, geography, unit, numerator/denominator, evidence type and reuse terms. Do not submit private data, invented facility attributes or restricted source documents. Preserve original units and nulls.

Run `python scripts/reproduce.py`. Explain changed formulas and uncertainty assumptions. Keep observations separate from illustrative inputs. A new country or facility needs a documented source and boundary; a coordinate alone is not a water supply link. Corrections are welcome and should appear in the changelog.

## Source and frontend ownership

Edit browser source modules in `dist/`; `scripts/build.py` regenerates the website copy in `docs/`. Do not hand-edit the generated copy. Run `python scripts/reproduce.py` before submitting. Source refresh now creates candidates; follow [source review](docs/source_refresh.md) before promotion. Never promote downloads merely because an anchor string matched.
