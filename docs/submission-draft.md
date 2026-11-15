# AstroCare AI — project submission draft

Team: **AKYILDIZ**<br>
Prepared: **15 November 2026**<br>
Status: **Draft for Scrum Master approval. Not submitted.**

## Project title

**AstroCare AI — Health Trends and Space Research in Context**

Selected challenge, as recorded by the team: **Create Health Monitoring Software
for Astronauts on Space Missions**, NASA Space Apps Challenge 2026. Membership of
the selected dataset in the official challenge Resources list remains unverified.

## Short project summary

AstroCare AI is a multilingual Streamlit prototype that makes health-related
measurements easier to explore while making their limitations visible. A fictional
mission dashboard tracks sleep duration, resting heart rate, and activity using
reproducible synthetic records and optional fictional manual entries. A separate
explorer presents authentic NASA-hosted Inspiration4 serum research measurements
with exact values, units, sampling context, and verifiable source provenance.
These workspaces never combine their records. AstroCare provides descriptive
analysis, not clinical monitoring, diagnosis, or treatment advice.

## Problem being addressed

A health dashboard can display numbers without explaining what they represent,
how complete they are, or which conclusions the data cannot support. Space-related
research also involves discrete laboratory samples that should not be presented
as continuous health telemetry. Our prototype addresses these interpretation and
communication problems with readable trends, explicit source separation, and
accessible scientific context.

## Our proposed solution

The **Health dashboard** demonstrates a possible monitoring interface with clearly
labeled fictional data. Users inspect daily values, previous-day differences,
seven-day means, observation counts, and comparisons between separate seven-day
periods. The **NASA Research Explorer** provides a distinct view of scheduled
pre-flight and post-flight serum measurements. It preserves the original units and
values, with shared zero-based comparison scales and expandable provenance.
Neither view generates diagnoses, medical risk scores, or clinical conclusions.

## Working features

- Twenty-one reproducible fictional daily records and a fictional crew profile.
- Sleep, resting-heart-rate, and activity summaries; independently selectable
  charts; date/range controls; daily tables and seven-day comparisons.
- Missing, invalid, and explicit-zero values remain distinct; no imputation.
- Validated fictional manual entry with local SQLite persistence and duplicate
  protection. Real personal health or identifying information must not be entered.
- Separate, offline OSD-575 exploration after explicit local preparation.
- Pre-/post-flight serum cards with exact numeric labels, original units, honest
  missing states, and one common zero-based scale per selected analyte/participant.
- File-integrity checks, acquisition receipt, source links, checksums, and visible
  distinctions between synthetic telemetry and authentic biospecimen research.
- English, Turkish, French, German, and Spanish interfaces; expandable safety,
  methods, scientific-context, and provenance information.

## Technology stack

Python **3.11.9**, Streamlit **1.67.0**, Pandas **3.1.1**, Plotly **7.1.0**,
pytest **9.2.0**, and Python's built-in SQLite support. The research cards use
escaped HTML and scoped responsive CSS. Dependencies are pinned in
[`requirements.txt`](../requirements.txt).

The product name does not indicate a running AI model. No Ollama or other AI
inference service is integrated.

## Exact NASA OSD-575 data usage and limitations

Source: [NASA OSDR OSD-575 study](https://osdr.nasa.gov/bio/repo/data/studies/OSD-575),
version **3**, DOI **10.26030/mc5d-p710**. The study is titled *SpaceX Inspiration4
Blood Serum Metabolic Panel and Immune/Cardiac Cytokine Arrays (Comprehensive
Metabolic Panel and Multiplex)*.

The application uses only
`LSDS-8_Comprehensive_Metabolic_Panel_CMP_TRANSFORMED.csv`, matched against the
study's sample metadata. The reviewed file contains **28 serum samples from four
published participant pseudonyms**, with **58 original columns**. The explorer
selects **112 analyte observations**: albumin (g/dL), glucose (mg/dL), sodium
(mmol/L), and creatinine (mg/dL).

Visits are **L-92, L-44, L-3** before launch and **R+1, R+45, R+82, R+194** after
return. Launch and return are different anchors. R+194 is explicitly present in
the CSV and sample metadata but is not included in the shorter narrative study
schedule; this discrepancy remains disclosed. No intermediate measurements,
paired comparisons, or continuous daily timeline are inferred.

The original CSV SHA-256 is
`5eb1e7f025dd8443a9e70111e62bc32afae3432753024489c5c013e401d709d9`.
Source URLs, metadata checksum, unit mappings, and licensing evidence are pinned
in the measurement-free [manifest](../data/osd575_manifest.json). The reviewed
study record lists **CC0-1.0**, and acquisition checks that the selected file is
unrestricted and matches its official URL. Raw CSV, metadata, receipt, and local
scientific review documents are excluded from public Git delivery.

Reproduce preparation from the project root:

```powershell
.\.venv\Scripts\python.exe -m astrocare.acquire_research
```

Prepared snapshots work offline. Missing or changed files stop numerical research
display instead of triggering a synthetic fallback. An upstream file change
requires separate review; checksums are not automatically updated.

These are Inspiration4 commercial crew research samples, **not live NASA career
astronaut telemetry**. The CMP file contains no daily sleep duration, resting
heart rate, or activity minutes. Those three dashboard metrics remain synthetic.

## Scientific evidence and safety limitations

Scientific review status remains **CORRECTIONS REQUIRED**. No separate documented
scientific acceptance has been issued in this delivery. Technical tests and the
Scrum Master's UI acceptance do not constitute scientific approval.

Linked NASA sleep, cardiovascular, and exercise research provides background
context, not validated clinical thresholds for this application. The interface
separates observed data, calculated summaries, prototype rules, published context,
and their limitations. Small sample size, incomplete measurement context,
unverified sensor accuracy, sleep duration versus sleep quality, and activity
duration versus physiological outcomes remain material limitations.

No clinical validation, NASA endorsement, operational flight readiness, medical
risk scoring, medication advice, or confirmed official Resources compliance is
claimed. The integrity badge verifies prepared local files, not scientific merit.
See the [scientific correction matrix](scientific-corrections.md).

## What makes the prototype useful

AstroCare provides a working, inspectable way to explain health trends without
hiding missing data or overstating scientific certainty. Judges can switch chart
views, compare periods, inspect exact serum values, and trace measurements to
their source. Clear separation of fictional monitoring and authentic research
helps demonstrate both interface utility and responsible interpretation.

## Repository and delivery status

[GitHub repository](https://github.com/Aerophis/nasa-space-apps-2026-Akyildiz-Health-Monitoring-Software-for-Astronauts)

Last delivered Sprint 3 baseline:
[`ddafe06378e4ed126c0393bffefa5a80fc0c078d`](https://github.com/Aerophis/nasa-space-apps-2026-Akyildiz-Health-Monitoring-Software-for-Astronauts/commit/ddafe06378e4ed126c0393bffefa5a80fc0c078d).
Sprint 4 changes and this draft are local pending explicit approval. There is no
public deployment URL. A demo video and presentation have been planned, not
recorded, rendered, or submitted.

## AI-assisted development and verified roles

Codex assisted with implementation, translations, tests, documentation, and QA
under the team leader's instructions. The code is not represented as entirely
hand-written by the team. The README records earlier personally authored
contributions according to the team leader's declaration; no additional authorship
or scientific approval is inferred here.

| Role | Verified attribution and limit |
| --- | --- |
| Team leader / Scrum Master / main developer | The user supplied scope and design direction, reviewed the working dashboard, and accepted the latest UI. Final delivery approval remains separate. |
| Python development and testing | Muhammed Ali was identified for this role by the team leader. No additional completed Sprint 4 contribution is asserted without evidence. |
| Scientific research and validation | A scientific research teammate was identified by the team leader; existing review findings are documented. No new scientific acceptance is claimed. |
| AI development assistance | Codex performed authorized software, QA, and documentation work under the lead's direction; it is a tool, not a human team member. |
