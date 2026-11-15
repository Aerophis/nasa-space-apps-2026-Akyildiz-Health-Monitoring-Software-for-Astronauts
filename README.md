# AstroCare AI

**AKYILDIZ · NASA Space Apps Challenge 2026**

Challenge: [Create Health Monitoring Software for Astronauts on Space Missions](https://www.spaceappschallenge.org/2026/challenges/health-monitoring-software/).

AstroCare AI is a Streamlit prototype for exploring changes in sleep duration,
resting heart rate, and exercise/activity duration during a fictional space mission.
It provides descriptive summaries, not diagnoses, disease predictions, medical risk
scores, medication advice, or treatment recommendations. It is not NASA-approved
or clinically validated.

> **DEMO — SIMULATED DATA**
> Health dashboard records are fictional. Do not enter real personal health data or identifying information.
> The separate research explorer displays verified public NASA-hosted biospecimen data after local preparation.
> Scientific review status: **CORRECTIONS REQUIRED**.

## Current features

- A fictional crew profile and 21 reproducible daily records, dated 25 October–14 November 2026.
- Three summary cards, interactive Plotly charts, daily records, and date/range selection.
- Previous-calendar-day changes, 7-day averages, and valid observation counts.
- Separate classifications for missing, invalid, and valid measurements; missing values are not counted as zero.
- A manual form for a separate fictional profile, with date, unit, type, provenance, and duplicate checks.
- Local SQLite persistence; existing records are never silently overwritten.
- Comparisons between two non-overlapping 7-day periods. At least 5 comparable records per metric in each period are required before a descriptive comparison is shown.
- Deterministic explanatory messages, source labels, and demo labels embedded in chart images.
- A separate OSD-575 research explorer for four serum analytes, with sample context,
  original units, license/source information, checksums, and offline loading.
- Source-backed context cards separating observations, calculated trends, prototype
  rules, and published research context.
- A brighter navy interface with readable summary cards, multi-select chart
  visibility, and expandable evidence, methodology, and provenance details. Sleep uses
  an area chart, heart rate a line chart, and activity a bar chart; NASA serum
  research uses compact pre-/post-flight cards with thin horizontal bars, exact
  numeric labels, and one shared zero-based scale. Cards stack on narrow screens.
- English (default), Turkish, French, German, and Spanish interface options.
  Seven-day coverage bars describe available numeric records, not health scores
  or medical targets. Language changes preserve data and selected filters.

The 5-record requirement and duration/date limits are demo design and data-format
rules, not clinical thresholds. Manual resting-heart-rate records without confirmed
fictional resting conditions are excluded from period comparisons.

## Technology stack

Python 3.11.9, Streamlit, Pandas, Plotly, pytest, and Python's built-in SQLite support.
Exact package versions are pinned in `requirements.txt`.

## Installation on Windows

Open PowerShell in the project root. For a fresh checkout with Python 3.11.9 available:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If the prepared `.venv` already exists, use it directly. Activating it is optional
because the commands below explicitly invoke its Python executable.

## Launch

Run from the project root:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501). Stop the server with `Ctrl+C`.
If PowerShell cannot find the relative executable path, first navigate to the
project directory. For the team's current Windows workspace:

```powershell
Set-Location -LiteralPath "C:\Users\Ynigh\Desktop\Nasa Spaceapps Challange"
```

## Testing

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check
```

Tests use temporary databases and research directories rather than local application
data. Final Sprint 4 QA on 15 November 2026 recorded **228 passed in 13.83s**.
All prior 224 scenarios remain covered, including shared-scale cards, source
precision, missing data, and HTML escaping. Four additional cases verify that
invalid CSV, metadata, acquisition receipt, or manifest files withdraw the verified
indicator. Historical results
and their limitations are documented in the sprint reports. Tests do not establish
clinical validity or scientific acceptance.

## Demo data and local storage

The generated `DEMO-001` dataset uses seed 2026 and is not modified by manual
entries. The form accepts invented records for `DEMO-MANUAL-001` only. Both
sources retain `is_synthetic=True`; they are never combined or presented as NASA data.
Blank measurements remain missing; explicit zero sleep/activity duration is a
valid numeric record. Invalid records and duplicate dates are rejected.

The database `local_data/astrocare.sqlite3` is created on the first successful
manual save and persists across restarts. SQLite files and sidecars, the virtual
environment, caches, and secrets are ignored by Git. `ASTROCARE_DB_PATH` can
select another local database for development or testing. Encryption, real patient
data handling, multi-user access control, record editing, and deletion are not supported.

## Scientific limitations and NASA data status

**A real NASA-hosted OSD-575 CMP file is integrated locally in a separate research explorer.**
It contains scheduled serum samples from Inspiration4 commercial crew, not daily
sleep/heart-rate/exercise telemetry or NASA career astronaut monitoring. The three
health dashboard metrics remain fictional. The official challenge Resources list
and eligibility still require verification. No clinical acceptance is claimed.
See the [NASA data research log](docs/nasa-data-research.md).

Prepare the reviewed local snapshots once, with internet access:

```powershell
.\.venv\Scripts\python.exe -m astrocare.acquire_research
```

Then choose **NASA Research Explorer** in the application's **Workspace** selector.
The explorer works offline after preparation. A missing, changed, or invalid file
shows a clear error rather than simulated replacement values. Raw CSV and metadata
remain under ignored `research_data/OSD-575/`; they are not proposed for GitHub delivery.
The public [manifest](data/osd575_manifest.json) pins the reviewed schema and checksums.
The source study lists CC0-1.0 and the file API marks this CSV unrestricted; acquisition
and licensing evidence are documented in the research log.

The serum plot uses categorical sampling visits: L− means days before launch and
R+ means days after return, verified against the prepared sample metadata. Launch
and return are distinct reference events. Separate cyan pre-flight and coral
post-flight cards identify the published participant, analyte, unit, visits, and
exact measured values. Both use the same zero-based scale, calculated jointly
from the selected measurements with modest display headroom; phases are never
normalized independently. This scale is not a clinical reference range or target.
Missing results have an explicit label and empty dashed track, distinct from a
measured zero. No intermediate visits or paired comparisons are inferred.
Use **View measurements** and the source/context expanders for records and
provenance. Fluctuations are not interpreted as clinically significant.

The compact header shows **Verified NASA-hosted data** only after local file
checksums, schema, and acquisition receipt pass validation. This indicates local
snapshot integrity, not NASA endorsement or scientific acceptance. **Research
only · Not clinical monitoring** and the separation from synthetic health
telemetry remain visible. Full limitations and **CORRECTIONS REQUIRED** remain
accessible in **Safety & Scientific Review**, **Study Context & Limitations**, and
**Dataset Details · Source & License**.

Technical test success does not constitute scientific acceptance or clinical
validation. The prototype does not establish sensor accuracy, diagnose conditions,
or infer muscle/bone health from exercise duration. General adult health guidance
is not an astronaut clinical alarm threshold. Scientific review remains
**CORRECTIONS REQUIRED**, with unresolved issues recorded in the sprint reports.

## AI-assisted development and contributions

Codex generated the initial prototype and the original 21 tests under the team
lead's direction. The team lead reported personally adding the `sleep_hours`
calculation and two tests in Sprint 1, followed by `classify_sleep_minutes()` and
six tests in Sprint 2. Those contributions are present in the repository; individual
authorship is attributed according to the lead's declaration.

With explicit authorization, Codex implemented the remaining Sprint 2 software,
integration, and additional tests. These AI-assisted contributions are not described
as code written entirely by hand by the lead. The product name does not imply a
running AI model: no Ollama or other AI inference service is integrated.
Sprint 3 research loading, parsing, UI, scientific-context cards, and tests were
also developed with Codex assistance under the lead's explicit authorization.
Sprint 4 presentation, regression tests, and delivery documentation were developed
with Codex assistance following the Scrum Master's design direction. Scientific
acceptance and GitHub delivery remain separate review decisions.

## Project documentation

- [Local development and data rules](docs/development.md)
- [Sprint 1 historical review](docs/sprint-1.md)
- [Sprint 2 implementation report](docs/sprint-2.md)
- [NASA data research and follow-up work](docs/nasa-data-research.md)
- [Scientific correction matrix](docs/scientific-corrections.md)
- [Sprint 3 implementation report](docs/sprint-3.md)
- [Sprint 4 UI/UX and final QA report](docs/sprint-4.md)
- [Local demo and delivery checklist](docs/demo-checklist.md)
- [Project submission draft](docs/submission-draft.md)
- [30-second English demo storyboard](docs/demo-storyboard.md)
- [Seven-slide English presentation outline](docs/presentation-outline.md)

Local scientific PDF/DOCX documents under `docs/research/` are excluded from the
proposed delivery. Their presence locally is not permission to redistribute them.
