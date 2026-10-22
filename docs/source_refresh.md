# Refresh and review source captures

A download attempt never overwrites the reviewed registry or processed data. Successful bytes are stored by source ID and SHA-256 under ignored `data/raw/captures/`; each run writes an attempt record under `data/raw/refreshes/`. Failed attempts remain inspectable without destroying the last-good snapshot.

```powershell
python scripts/ingest.py --refresh
```

Open the downloaded source yourself, check the exact locator, units, period, reporting scope and changed definitions. Inspect the run's `attempt.json`. To promote one reviewed capture, supply the printed run path and exact candidate hash:

```powershell
python scripts/review_refresh.py --run data/raw/refreshes/YOUR_RUN --source-id SOURCE_ID --sha256 EXACT_64_CHARACTER_HASH --reviewer 'Your name' --note 'Exact pages/tables reviewed, definitions checked, changes and caveats'
python scripts/reproduce.py
```

The placeholders must be replaced; they are not valid verification evidence. Promotion rejects a mismatched hash or a registry edited since download. A review record binds the URL, bytes, locator, scope, reviewer and dates; prior captures are archived. Existing legacy records retain their original metadata rather than receiving invented review identities.

Promotion of CGWB also parses its candidate table before updating the pointer. Changed factual claims still require review and deliberate edits; promotion is not automatic claim extraction or independent assurance. Inspect the resulting Git diff before committing. Raw third-party bytes stay out of Git. The build manifest now includes nested review JSON as well as the main registry.
