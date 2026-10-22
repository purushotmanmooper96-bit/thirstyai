# Explain the work in an interview

## Thirty seconds

I built an independent analytical project about data-centre water accounting. It combines six primary sources, a reproducible India groundwater extraction and an interactive trade-off model. The important design decision was to keep reported observations separate from assumptions and to reject incompatible water definitions. I tested the same calculations in Python, JavaScript and SQL rather than trusting a dashboard alone.

## Decisions to explain

- Why withdrawal WUE cannot be used for a consumption claim.
- Why IT and facility energy need distinct denominators.
- Why we preserve a source's published ratio when its rounded volumes cannot reproduce it.
- Why we don't publish facility or global water rankings without the corresponding data.
- Why SQLite is the runnable audit path and PostgreSQL/Power BI execution is disclosed as unverified.

## Resume bullet after reviewing and understanding the implementation

Built ThirstyAI, an independent water–energy analytics project, using Python, SQL and an interactive web dashboard; extracted 36 Indian state/UT records, documented six primary sources, and verified accounting consistency across Python, JavaScript and SQL.

Use only if you can explain the code and actually reproduce it. Do not claim real-world liters saved, employer sustainability experience, public adoption or independent assurance.
