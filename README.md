# AstroCare AI

**AKYILDIZ · NASA Space Apps Challenge 2026**

Challenge: [Create Health Monitoring Software for Astronauts on Space Missions](https://www.spaceappschallenge.org/2026/challenges/health-monitoring-software/).

AstroCare AI is a Streamlit prototype for exploring changes in sleep duration,
resting heart rate, and exercise/activity duration during a fictional space mission.
It provides descriptive summaries, not diagnoses, disease predictions, medical risk
scores, medication advice, or treatment recommendations. It is not NASA-approved
or clinically validated.

> **DEMO — SIMULATED DATA**
> All supported records are fictional. Do not enter real personal health data or identifying information.
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

Tests use temporary databases rather than the local application database. The
Sprint 2 implementation run recorded **104 passed in 2.95s**; historical results
and their limitations are documented in the sprint reports.

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

**Real NASA health data or telemetry has not been integrated.** Official challenge
Resources verification, suitable file selection, licensing, and field mapping
remain open. OSD-575 has not been treated as a sleep/heart-rate/exercise time series.
See the [NASA data research log](docs/nasa-data-research.md).

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

## Project documentation

- [Local development and data rules](docs/development.md)
- [Sprint 1 historical review](docs/sprint-1.md)
- [Sprint 2 implementation report](docs/sprint-2.md)
- [NASA data research and follow-up work](docs/nasa-data-research.md)

Local scientific PDF/DOCX documents under `docs/research/` are excluded from the
proposed delivery. Their presence locally is not permission to redistribute them.
