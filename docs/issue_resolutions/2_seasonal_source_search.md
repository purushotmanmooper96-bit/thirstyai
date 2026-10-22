# Issue 2: seasonal source discovery

Status: **source-discovery acceptance met**. [NREL operator report, September 2018](https://docs.nlr.gov/docs/fy18osti/72196.pdf), Figure 4 (printed p.6 / PDF p.13), publishes monthly cooling-tower water for the named ESIF HPC Data Center in Golden, Colorado, September 2016–August 2017. Section 2.2 (printed p.5) separates observed use from estimated savings. Section 3.2.1 (printed pp.10–11) explains metering and excluded humidification.

The publisher's “consumption” includes supply associated with sewer flows; it must not be equated to net evaporative consumption. This is one historical HPC facility, not an AI-only or drought-impact result. Monthly volumes were not digitised. No headline or facility row is added.

[Download hash, UTC time, licence and review record](../../research/reviews/issue_2_nrel_seasonal.json). Text and rendered chart checked; raw PDF/figure excluded. Free access does not establish a broad reuse licence. Author review remains welcome.

Verification: `python scripts/reproduce.py`. PowerShell after updating: `git pull --ff-only`, then that command.

## Earlier candidate, retained as rejected context

Reviewed candidate: [City of The Dalles, Seasonal Water Supply Monitoring Update, 13 October 2026](https://www.thedalles.org/news_detail_T4_R275.php). Exact sections: WATER DEMAND AND SYSTEM USAGE, MONTHLY SNAPSHOT, DROUGHT & WATERSHED CONDITIONS, WHO THIS INFORMATION APPLIES TO.

The official page describes seasonal supply, conservation and a monthly comparison for the municipal utility's customers. The entire service area is the boundary. A linked water-use graph could not be downloaded (HTTP 403), so its figures were not transcribed. The page does not provide a verified named-data-centre monthly withdrawal/consumption series. Calling city-wide use Google's facility use would be an attribution error.

[Capture and review record](../../research/reviews/issue_2_seasonal_candidate.json) retains the direct URL, date, exact section locator, raw-byte SHA-256, UTC retrieval time, licence note and confidence. Raw documents are excluded. No numeric water claim is promoted. UNVERIFIED applies to the sought facility-level series, not to the fact that the city page was retrieved and inspected.

Other inspected search results included monthly billing pages and proposed reporting requirements; these do not provide an observed facility series and were not promoted. Next useful evidence is a public utility meter table, official permit return or operator monthly disclosure naming the site, months, units and water definition. No emails or records requests have been sent on the author's behalf.
