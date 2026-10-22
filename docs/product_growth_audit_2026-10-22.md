# ThirstyAI: product, growth and architecture audit

Reviewed 22 October 2026 at main commit a90ffbed977d23dd1deb794ab6a561895c86faeb. Audit and proposed copy only: no application fixes, README replacement, release or social posting performed in this review.

## Scope and evidence

Read the current GitHub README and metadata, repository tree, browser/model code, Python engine, ingestion/build/validation scripts, SQL/PostgreSQL verification, workflows, tests, BI/workbook documentation and previous QA. Inspected the public overview and lab in Chrome. Reran offline reproduction: 53 Python tests, 7 JavaScript tests, integration parity, notebook/syntax/link checks; generated tracked files remained unchanged. Main run 39780278743 has successful Windows, Linux, PostgreSQL and Lighthouse jobs; Pages deployment 39780277705 succeeded. This is not a full penetration test, independent environmental audit or real-user retention study.

Repository API snapshot: zero stars, zero forks, twelve topics, no published GitHub releases. README length: 1,634 whitespace-separated words. Initial assets measured locally: 165,217 uncompressed bytes, including navigation.mjs; not CDN transfer size or field performance. Custom social-preview image is already 1200×630. Do not present previously fixed discoverability/CI/social-card items as still missing.

Issue #5 is now closed as completed on GitHub. Its two comments still state that native Excel execution and author confirmation are pending; no confirming report/screenshots were found in that thread. Closed state is not validation evidence. Historical limitations.md is explicitly v0.1; do not silently rewrite it in conflict with the author's confirmation requirement. Maintain a clearly linked current validation summary.

Verdict: a credible small evidence project with an underdeveloped public product. The most valuable feature is careful comparability, not another dashboard page. Current low engagement is not proof of rejection; traffic and retention analytics were not available. Product/growth assessments below are hypotheses supported by observed friction, not measured bounce rates.

## 1. The 3-second test

ThirstyAI is memorable but ambiguous: it could be an AI assistant, prompt-footprint meter, or water tool using AI. The current hero, “AI runs on code. The cloud runs on resources,” describes a theme without promising a task or result. “Evidence atlas & decision lab” sounds institutional. The name need not change; the descriptor should.

Recommended descriptor: **AI water evidence, explained.**

Three headline candidates:

1. **See what AI water headlines leave out.**
2. **Compare AI water claims. Check what the numbers mean.**
3. **Less cooling water. More electricity. What changes overall?**

Use the first for the public landing page, the second for the company-reporting entrance, and the third for the simulator. These are copy hypotheses, not proven high-conversion headlines. Lead with the public question, one concrete example, one action. Retain a short boundary beside the result and put supporting methodology one click deeper.

Choose one initial audience: people checking AI-water claims—curious developers, students and journalists. Analysts can then inspect/download the evidence. Do not try to greet the public, engineers, regulators, researchers and recruiters with equal priority.

## 2. Product and UX friction

| Observed friction | Consequence | Specific change / acceptance |
|---|---|---|
| Eight navigation destinations | New visitor chooses a curriculum before learning the payoff | First screen offers “Understand one claim” and “Try a cooling trade-off”; specialist views stay in navigation |
| Water-branded hero followed by electricity projections and a row count | Visitor still has not seen what the product uniquely explains | Put a water-report boundary example above the fold; keep energy context below |
| Primary CTA opens a nine-input lab with technical labels | User must already understand the model | Start with a guided hypothetical example; reveal advanced controls on demand |
| Results follow the input panels | Visitors must scroll to see the answer | Put a short result summary before controls; sticky summary on mobile |
| No guided explanation of the supplied baseline/alternative | Defaults can feel arbitrary | Explain that these are assumptions; offer a “show electricity-related water” reveal |
| Sliders have no paired exact-value fields | Harder precise exploration | Add bounded numeric inputs with unit labels alongside sliders |
| Dense mixed-metric company table | Reading effort overwhelms the comparison | Filters for company/metric, compact cards, expandable scope/locator details; preserve full accessible table/download |
| Google gallons versus other operators' ML | Casual readers cannot compare magnitude | Offer clearly labelled unit conversion while retaining source units; conversion must never remove scope/year mismatch flags |
| Location view displays only overlay matches | Seven location records exist but only five matched rows are visible | Show all curated rows; unmatched rating is “Unknown,” never safe |
| India context has weak direct connection to the primary task | Feels like an extra portfolio dataset | Make it a clearly labelled regional context study, with a data-centre siting question and explicit missing linkage |
| Readme explains everything before giving a demonstration | Technical depth acts like entry friction | Two-minute front door; preserve full background and action evidence in docs |
| No visible update subscription or dependable change log experience | Most visitors have no reason to return next week | Ship a small “what changed in the evidence” page and dated updates; do not claim live monitoring |

**Reproduced defect:** In #lab, clear the IT workload field. The validation message appears, but prior results remain visible and Export result remains enabled. Share also still reads the last valid state. A visitor can export an answer while the visible input is blank. Fix by marking results unavailable or explicitly “last valid result,” disabling share/export while invalid, and restoring them only after successful recalculation. Add a browser regression for clear, invalid, corrected, then export.

The app does not call an LLM: calling it an AI wrapper would be inaccurate. But visual branding alone cannot establish originality. Demonstrate a definition rejection, a traced report locator and a reproducible cross-language calculation. Do not add a chatbot, 3D globe, invented city leaderboard or personal litres-saved counter to look more advanced.

Retention should fit the product. An evidence reference may succeed through citations, reuse and return visits when reports change; daily streaks are not inherently valuable.

## 3. The viral loop

The lab already has Copy scenario link and exports. The missing feature is not any sharing at all: it is a small result worth sharing. Today a screenshot captures dashboard chrome, technical inputs and partial context. The generic Open Graph card does not explain a specific shared scenario. Hash routes do not provide unique server-rendered social metadata. No share analytics were observed, so actual sharing rate is unknown.

### Mechanic A: “Show your assumptions” receipt

Trigger: after a valid comparison, offer **Download result card** and **Copy reproducible link**.

Card: plain-language question; direct water, electricity-related water, total water and energy change; “ILLUSTRATIVE SCENARIO — NOT A FACILITY MEASUREMENT”; workload and critical factors; model version; ThirstyAI URL. These must remain visible on the exported image. Use PNG plus accessible text. No company logos attached to hypothetical bundles.

Recipient loop: opens the exact versioned inputs, sees the same result, changes one assumption and makes another receipt. Add a compact, validated and versioned share payload; preserve model version/rounding. Current static hosting can generate images client-side. Distinct rich previews would require pre-generated share pages or an explicitly designed preview service; do not promise arbitrary dynamic OG previews from hash changes.

Acceptance: screenshot remains interpretable outside the app; two independent opens reproduce it; tampered/invalid links fail safely. Measure actual card downloads, shared-link arrivals and completed comparisons. Do not equate a copy-button click with a publicly posted share.

### Mechanic B: “Can these numbers be compared?” challenge

Trigger: show two genuine source-backed disclosures with their period, scope and metric. Ask “Comparable as shown?” Reveal the explanation, missing denominator and original locators after one tap.

Share: “I spotted the missing boundary” card with answer spoiler optional, explanation URL and source IDs. Recipient tries a different pair and can suggest a correction. Score only understanding of documented definitions—not company ethics, environmental harm or an invented “green score.” No login, forced sharing or vote-for-access.

Start with three carefully authored questions. Test whether people understand them before adding a quiz engine. Company evidence must stay separate from fictional lab results. The growth loop is useful correction and learning, not manufactured outrage.

## 4. GitHub and README makeover

The current README is careful and useful as background, but too long for a front door. There is no early product demonstration. Some docs describe earlier validation checkpoints; validation_v02.md still says five contribution issues are open. Two changelogs and multiple launch/audit files make the current status hard to locate. dist/ is frontend source as well as distributable output; docs/ mixes Markdown and a generated website copy.

Strengths to retain: standard-library Python core, explicit accounting dimensions, small static app, provenance, CI across Windows/Linux, actual PostgreSQL comparison, documented dataset limitations, CI/license badges and twelve topics. A custom social card already exists.

Recommended repository changes, in order:

1. Put the demo, single useful task and a current demonstration image/video near the top.
2. Use the complete root-level README.proposed.md supplied with this audit. Preserve today's long explanations in a public guide before replacing the current README.
3. Create one current validation matrix linking historical checkpoints. Record issue status separately from engine-verification status.
4. Publish a tested, immutable GitHub release with processed snapshots, checksums and scoped notes. Release notes currently exist, but no published release was returned by the API.
5. Document that editing dist/ is authoritative and docs/ is generated. Later, move frontend source to web/ and generate the Pages artifact; do not duplicate hand-edited sources.
6. Maintain one canonical changelog and one contributor entry point. Move superseded audit records under an archive with clear dates, retaining their evidence.
7. Add a few new bounded contribution tasks now that the original issue list is closed. “Verify one locator” is better than “make project viral.”

The proposed README describes implemented features only. Image cards and challenges are roadmap recommendations, not shipped features. GitHub stars are a follow mechanism, not proof of engineering quality or hiring suitability.

## 5. Code and architecture red flags

| Priority | Finding and evidence | Fix and meaningful verification |
|---|---|---|
| P1 | Invalid workload leaves stale results/export enabled: dist/app.mjs bindLab; reproduced on public site | Explicit valid/invalid state; disable exports/sharing and label stale output. Browser test the full invalid-to-valid transition |
| P1 | scripts/ingest.py replaces provenance.json before checking failures | Stage captures in a run directory; preserve last-good evidence; write an attempt log separately; promote atomically after approval. Regression: simulated network failure leaves all reviewed snapshot bytes unchanged |
| P1 | Refresh approval is a source-ID/hash match against a mutable single record; changed bytes need an explicit review workflow | Immutable per-capture records and review manifest binding reviewer, locator, hash, date and scope. Build accepts only reviewed captures, with preserved history |
| P2 | Future CSV lacks full WUE/grid/carbon inputs and model version: updateFutures | Export complete assumptions, boundary and version; test reconstructing outputs from the export alone |
| P2 | Evidence fetch failure replaces static HTML with an error then throws: app.mjs initial fetch catch | Keep the crawlable evidence, disable interactive controls and offer retry/downloads; test fetch failure rather than only successful snapshots |
| P2 | Frontend combines routing, state, templates, exports and event binding in a small number of very long lines | Split router, evidence views, lab, share codec and exports into readable modules; preserve deployment simplicity |
| P2 | Existing tests cover arithmetic well but miss real interaction transitions | Add browser cases for invalid/stale state, copy-link round trip, query reset, fetch failure, filters and export reconstruction |
| P2 | Hard-coded release/review labels, old QA summaries, duplicate changelogs | Generate current labels from release/source metadata; show historical measurements as historical; check documentation status consistency |
| P2 | Main manifest hashes only top-level research JSON; nested issue review JSON is omitted | Hash promoted review records recursively or explicitly distinguish them as source-discovery-only material; test capture-to-review linkage |
| P3 | Actions use mutable major tags; npm Lighthouse version is fixed but transitive installation has no lockfile | Pin action commits, explicit read permissions for validation and locked audit dependency graph; update deliberately |
| P3 | Escaping is present, but source URLs are not protocol-allowlisted by the evidence validator | Permit expected https/http source URLs; reject javascript/data schemes; malformed contributor metadata test. No exploitable public upload path was found |

Refresh defect was tested offline in a temporary directory with a synthetic source and simulated TimeoutError. The old reviewed capture was replaced with a fetch_failed entry before SystemExit. No real source endpoint was stressed and no live research data was changed.

Security scope: no real production API key was found in the inspected files. The PostgreSQL password is an explicit ephemeral CI service credential, not evidence of a leaked production password. This was a targeted tracked-file review, not exhaustive history/secret scanning. Notebook execution is expected repository code execution; keep untrusted pull requests on isolated runners with no privileged secrets.

Scale: the app is static and calculations are client-side. The current data size is small. An API rate limiter, Redis or Kubernetes would not solve an observed bottleneck here. GitHub Pages does have hosting limits (currently a soft 100 GB/month bandwidth limit), so keep a portable static artifact and watch real transfer usage. No load test or public-CDN real-user performance study was performed. Growth would first stress evidence maintenance and trust, not database writes on each visit.

## 6. Seven-day launch and distribution plan

This is a seven-day learning launch, not a promise of virality. If minimum quality gates fail, use the slot for fixes and defer the public launch.

| Day | Ship / do | Distribution and measure |
|---|---|---|
| 1 | Fix stale lab outputs and transactional refresh; choose one primary audience and hook | Watch five people unfamiliar with the repo attempt one claim check. Record whether they can explain the result, not just say it looks good |
| 2 | Guided example, compact result summary, first receipt card; verify keyboard/mobile and shared-input round trip | Measure time to first correct explanation. Target a ten-second first insight as a design goal, not a claimed benchmark |
| 3 | Short README, current screenshot, 20–30 second demo, validation matrix and release | Publish one X demonstration: problem → action → result → caveat → demo link. Invite a specific source/UX correction |
| 4 | Fix the biggest observed friction | r/SideProject: show the working tool and explain the build trade-off; disclose authorship. r/datasets: share the actual attributed snapshot/source register, licence limits and missingness, with original-source links |
| 5 | Publish one original explanatory visualization | r/dataisbeautiful: plainly describe the data, mark your own visualization [OC], disclose sources/tools in first top-level comment, and link the source article. No sensational company ranking |
| 6 | Launch the interactive tool on Show HN if ready | Angle: an inspectable water-accounting lab that rejects incompatible definitions. Show real interaction and limitations. Write the HN title/comments personally; do not paste generated or AI-edited text or solicit votes/comments |
| 7 | Product Hunt, only if first-use tests are good; otherwise another iteration | Tagline angle: AI water evidence, explained. Gallery: one comparison, one modelled trade-off, one source trail. Ask for feedback, never upvotes. Review results and publish fixes |

Recheck each community's current rules at posting time. r/SideProject's fetched page did not expose explicit local rules, so promotion permission is not assumed. r/datasets requires ownership disclosure, prefers original sources and labels for synthetic datasets; don't advertise scenarios as observations. Product Hunt is secondary to a useful specialist launch; do not burn a day on leaderboard tactics if visitors cannot explain the result.

X hook formats to test, as factual drafts rather than proven winners:

- “Two AI water numbers. Different years, fleets and definitions. Here's what to check before comparing them.” Attach an evidence view.
- “Lower cooling water can come with more electricity. I built a tiny lab to inspect the trade-off.” Attach a hypothetical example with the warning visible.
- “I kept the unknowns in my AI-water dashboard. Here is the missing data I couldn't responsibly fill.” Attach the coverage view.

Do not use tragedy, fake scarcity, “every prompt wastes X,” paid/bought votes, fabricated endorsements, “Google is hiding this,” or coordinated promotional replies. A credible correction is worth more than a sensational post that a researcher can dismantle.

Define funnel events before interpreting success: landing visit → first comparison/reveal → source opened → result exported/shared → shared-link arrival → recipient completes task. Attribute channels with campaign links and privacy-respecting aggregate measurement if implemented. Tracking was not present in the audited frontend. Record denominators; a copy click is not a share and a star is not a retained user. Track genuine corrections, independent reproductions and contributions alongside reach.

Subjective product-review scores, not market benchmarks: evidence discipline 8/10; reproducibility 8/10 within executed engines; first-use clarity 5/10; present shareability 3/10; differentiated usefulness 6/10. No honest method can assign a guaranteed viral probability from this repo review.

The highest-value next release is not bigger. It is one explained claim, one working comparison, one reproducible card and a clear path to verify or correct it.

## External sources checked for distribution/platform advice

- Show HN: https://news.ycombinator.com/showhn.html
- HN guidelines (including generated/AI-edited text restriction): https://news.ycombinator.com/newsguidelines.html
- Product Hunt official launch guide: https://help.producthunt.com/en/articles/17350772-launch-guide
- r/dataisbeautiful rules displayed in sidebar: https://www.reddit.com/r/dataisbeautiful/wiki/rules/ (requested wiki entry itself is absent; sidebar rules were readable)
- r/datasets displayed rules: https://www.reddit.com/r/datasets/
- r/SideProject inspected page: https://www.reddit.com/r/SideProject/
- GitHub Pages limits: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
- GitHub Actions security: https://docs.github.com/en/actions/reference/security/secure-use
