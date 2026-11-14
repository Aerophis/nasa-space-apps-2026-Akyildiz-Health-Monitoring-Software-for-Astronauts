# AstroCare AI — local development

Run from the project root in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Browser: [http://localhost:8501](http://localhost:8501). Stop with `Ctrl+C`.
Activation is optional: the command invokes the project virtual environment directly.
For installation instructions, see the [README](../README.md).

Run the tests and dependency check:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check
```

`astrocare/data.py` generates fixed-seed synthetic data and validates the daily
calendar and manual records. `astrocare/analysis.py` calculates daily changes,
7-day averages, and separate-period comparisons. `astrocare/charts.py` builds the
charts, `astrocare/storage.py` handles local persistence, and `app.py` provides the UI.

## Generated data and calendar rules

The generated demo has fixed dates: 25 October–14 November 2026. It is generated
in memory rather than downloaded. Calculations use UTC calendar days. The
generated profile and fictional manual profile remain separate. File upload,
external API ingestion into the health dashboard are not supported. The separate
Sprint 3 research explorer loads prepared public NASA-hosted samples without
merging them into these fictional records.

During daily preparation, records with invalid dates are excluded; if no valid
dates remain, an error is shown. Missing numbers are not estimated. Duplicate
calendar dates are rejected rather than silently combined. The 7-day window
includes the selected day. During the first days or when observations are missing,
the average uses fewer observations; cards show the count. These calculations
are not clinical validation or health advice.

Scientific links provide context; the synthetic measurements were not taken from
those sources. Detailed literature verification and scientific acceptance remain
separate team responsibilities.

## Fictional manual records

The **Data source** selector separates the 21-day **Generated demo** from
**Manual demo**. The form is for invented measurements only: do not enter real
identifying information or personal health data. Manual records also retain
`is_synthetic=True` and `source_type=manual_demo`; they are not appended to the
generated dataset.

- Open **Add a fictional manual health record** and enter the date and measurements.
- Sleep/activity use minutes and heart rate uses bpm. Decimal commas are supported.
- A blank field is missing data; 0 is an explicit, valid numeric sleep/activity record.
- At least one valid measurement is required. Any invalid measurement or a second record
  for the same date is rejected. Existing records are not automatically edited or deleted.
- Resting conditions can be confirmed for the fictional scenario. Unconfirmed heart-rate
  records remain visible in the daily table/chart but are excluded from period comparisons.
- A successful save selects Manual demo and refreshes the table, cards, and charts.

## SQLite storage

SQLite was chosen because it is included with Python and provides transactions
and a unique daily key to reject duplicates atomically. The default database is
`local_data/astrocare.sqlite3`. It is created on the first successful save; reading
an empty record list does not create it. Restarts read the same file.

The database and SQLite sidecars are covered by `.gitignore`. Local backup and
file management are the user's responsibility. Encryption and multi-user access
control are not implemented, so only fictional data are supported.

Tests set `ASTROCARE_DB_PATH` to temporary databases and do not write to the
project database. Developers may use that variable to select another local file.
Do not add local databases or scientific documents to Git. Avoid bulk `git add .`.

`validate_health_record()` checks dates, types, units, and provenance. The lead's
`classify_sleep_minutes()` function and six tests remain unchanged. A safe adapter
maps the existing `Valid`/`İnvalid` return values to the shared `valid`/`invalid`
statuses. The legacy `İnvalid` token is retained for API/test compatibility and
is not displayed in the UI.

## Period comparisons and limitations

The comparison uses the last 7 days including the selected day and the separate
preceding 7 days. Each metric requires at least 5 comparable observations in
each period. This is a demo design choice, not a clinical threshold. Missing
records do not contribute zeros to the average. When coverage is insufficient,
coverage information is shown instead of an interpretation.

Manual/generated sources and different profiles are never compared. Overnight
sleep calculations from start/end timestamps, planned exercise comparisons, and
assessment of actual sensor quality are not implemented.

Corrupt or unwritable databases produce readable errors; they are not deleted or
recreated over the original file. Chart images also retain demo and source labels.
Scientific review status remains **CORRECTIONS REQUIRED**.

## Language standard

New public documentation, sprint reports, UI content, and presentation material
must use professional English. Preserve proper names, source titles, file paths,
API identifiers, and historical evidence. Protected local research documents are
not translated or included in delivery. Sprint reports retain their original
implementation/review results; language review results are reported separately.

## Sprint 3 — separate NASA research workspace

```powershell
.\.venv\Scripts\python.exe -m astrocare.acquire_research
```

This explicit command obtains the reviewed unrestricted OSD-575 CMP CSV and study
metadata through the official NASA APIs, checks pinned SHA-256 values and schema,
and records acquisition details in `research_data/OSD-575/receipt.json`.
Existing files are not overwritten. If NASA changes the reviewed bytes, acquisition
stops for a separate version/schema review rather than accepting unknown data.
`ASTROCARE_RESEARCH_DIR` can select another local research directory.

The **Workspace** selector switches between the existing health dashboard and
**NASA Research Data Explorer**. The latter performs no network access and works
offline after preparation. Missing/checksum-invalid data produce errors and source
information only, never fabricated numerical observations.

`data/osd575_manifest.json` contains source/DOI/license notes, reviewed field names,
explicit analyte/unit mappings, expected shape, and checksum pins. No participant
measurements are stored in that manifest. The locally acquired raw files are ignored
by Git. Original study samples are validated against the study metadata rather than
guessed from a synthetic mission calendar.

The explorer selects albumin, glucose, sodium, and creatinine only. These are serum
assay observations, displayed as discrete sample markers with published pseudonyms.
L denotes days before launch; R denotes days after return. These are different time
anchors, not a continuous daily health timeline. R+194 is retained from the actual
CSV/sample metadata even though the narrative study summary describes fewer visits.
Reference-range and demographic/race-based derived columns are not interpreted.

`astrocare/research.py` handles offline validation/parsing; `acquire_research.py`
handles explicit network preparation; `research_ui.py` renders the separate view;
`science.py` provides deterministic, linked scientific context. Real research
records are rejected by the synthetic analysis/chart boundaries. The manual SQLite
schema and existing sleep classifier are unchanged.

Tests isolate both database and research directories. Small artificial parser fixtures
are test inputs only; they are not application fallback data. The local integration
was separately checked against all 112 selected values in the actual downloaded CSV.
Scientific status remains **CORRECTIONS REQUIRED**; see the correction matrix.
