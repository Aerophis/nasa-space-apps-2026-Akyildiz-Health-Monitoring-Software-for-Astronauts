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

Public documentation, sprint reports, and presentation material use professional
English. The interface defaults to English and supports Turkish, French, German,
and Spanish following the Sprint 4 correction request. Preserve proper names, source titles, file paths,
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
**NASA Research Explorer**. The latter performs no network access and works
offline after preparation. Missing/checksum-invalid data produce errors and source
information only, never fabricated numerical observations.

`data/osd575_manifest.json` contains source/DOI/license notes, reviewed field names,
explicit analyte/unit mappings, expected shape, and checksum pins. No participant
measurements are stored in that manifest. The locally acquired raw files are ignored
by Git. Original study samples are validated against the study metadata rather than
guessed from a synthetic mission calendar.

The explorer selects albumin, glucose, sodium, and creatinine only. These are serum
assay observations, displayed in phase-separated horizontal comparison cards with
published pseudonyms.
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

## Sprint 4 — presentation and local review

The palette and native control theme are in `.streamlit/config.toml`; the small
`astrocare/ui.py` module applies shared typography, cards, borders, and responsive
spacing. Tokens are shared with charts in `astrocare/theme.py`.
Solid navy surfaces and a solid header prioritize contrast over decorative effects.
No external fonts, decorative animation, or new
packages are required.

The **Visible charts** multi-select displays any one, any two, or all three health
charts stacked vertically; the default is all three. Clearing the selection shows
guidance without changing records or summaries. All three figures retain daily
values, the existing rolling series, original units, data gaps, and demo/source
annotations. Duration axes include zero; the heart-rate axis fits the observations
and is not a clinical reference range. NASA comparison cards use cyan pre-flight
and coral post-flight bars, with launch and return anchors distinguished.
Both panels use one shared zero-based scale, never independent phase normalization.
Summary counts describe participants, unique biospecimen samples, and selected
analytes; they are not health scores or treatment outcomes. Progress bars show
numeric-record coverage over the last 7 calendar days, not a medical target.

Long explanations are available under **Safety & Scientific Review**, **Evidence &
methods**, **How to read these charts**, and the research context/provenance
expanders. NASA source/version/license metadata now lives in **Dataset details ·
source & license**, below the main plot, rather than in the top overview. Sources,
checksum details, scientific limitations, sample records, and
manual entry remain accessible. Data analysis, validation, acquisition, and the
SQLite schema are unchanged. Health-chart calls remain compatible; research
presentation functions accept an optional language. The internal `research_chart()`
entry point now returns an immutable comparison model rather than a Plotly figure;
`astrocare/research_cards.py` renders escaped, responsive HTML from that model.

`astrocare/i18n.py` stores explicit English/Turkish/French/German/Spanish strings,
placeholder templates, and display-time translations of known domain messages.
The domain modules still return their original English messages and raw records.
No network translation service or new dependency is used. Unknown diagnostics
are explicitly labeled as original English technical detail, rather than guessed.
Technical field names, analyte names, published source titles, licensing evidence,
source codes, checksums, filenames, and identifiers remain original. Scientific
status **CORRECTIONS REQUIRED** and **DEMO — SIMULATED DATA** remain recognizable
in every language. The language choice is session-local; documentation stays English.

Formatted choices use locale-specific widget identities plus canonical selection
state in `astrocare/ui.py`. This refreshes cached native labels while preserving
workspace, source, date, range, and visible metrics across language changes.
Some framework-owned controls (for example, Plotly tools and Streamlit menu/date
picker chrome) can remain English. The catalogue is a prototype translation layer,
not an independently reviewed clinical translation or full framework localization.

The readability correction uses the Scrum Master's navy palette, with stronger
`#6986A0` interactive borders and `#78A8E8` focus outlines. Selected chips have a
dark `#1D354D` surface and `#F4F7FB` text/remove controls (11.71:1 computed contrast).
Normal text palette combinations target at least 4.5:1; interactive boundaries
target 3:1. These token checks and focused browser checks are not a full WCAG audit.
Metric accents are sleep `#78A8E8`, resting heart rate `#E4A17C`, activity `#6BD2B4`,
and NASA research `#65B8D2`. Dashed rolling averages remain visually secondary.
Figures use `theme=None` in Streamlit so explicit Plotly colors/fonts are retained.

NASA sampling semantics were checked in the original local metadata sample table:
`s_OSD-575-txt`, `Factor Value: Time` (field `a100011factorvaluetime`),
`Factor Value: Spaceflight` (field `a100015factorvaluespaceflight`), and time unit
`day`. `Launch minus 92/44/3` and `Return plus 1/45/82/194` are different anchors,
not a shared elapsed-days axis. Cards retain categorical visit labels and separate
phase headings without adding synthetic observations or connecting lines.
Row tooltips and accessible labels use the validated relative-day/anchor fields
and localized context. Source information remains in expanders rather than a
Plotly footer. **View measurements** retains the actual values, visits,
phase/context, units, pseudonyms, and provenance fields without modifying records.

The final comparison-card correction replaces the vertical-column research figure
entirely; no point-only or Plotly research chart remains. Every available visit has
one thin rounded bar with its label on the left and exact numeric value on the
right. A single ceiling is computed from both phases with 10% headroom, rounded
up to a readable decimal step. It is a display extent, not a clinical target.
Missing results use dashed empty tracks and localized labels; explicit zero is
still a valid value with zero-length fill. An absent phase remains visible with
an honest empty-state message; no visits are fabricated. All-zero/all-missing
selections use a shared display extent of 1, without substituting observations.
Nonfinite or negative values are rejected for this zero-based presentation rather
than clamped or altered. Source parsing, acquisition, and storage are unchanged.

Scoped CSS uses two columns above 760 pixels and stacked cards below; values
remain 18 px. Accessible heading roles avoid Streamlit's automatic heading links
and spacing. Every source-derived HTML text/attribute is escaped. EN/TR/FR/DE/ES
labels, source details, the sampling explanation, and measurement table remain
available. All previous 212 test scenarios were retained with presentation
assertions updated; 12 additional cases protect shared scaling, precision,
missing/empty states, invalid values, and escaping. Actual desktop and 390-pixel
English/German browser checks found no horizontal overflow. Health-dashboard,
analysis, validation, theme, and SQLite files were unchanged by this correction.

If an existing Streamlit process displays a **File change** notice, select **Rerun**
to refresh imported modules. A fresh process is preferable for final review after
theme changes. If port 8501 is in use, choose an available local port explicitly:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8502
```

The Sprint 4 review session uses [http://localhost:8502](http://localhost:8502).
This is a local session, not a public deployment; future launches may use another
available port. Browser smoke checks cover workspace/metric switching and a
390-pixel layout check, not an exhaustive accessibility or device certification.
See the [Sprint 4 report](sprint-4.md) and [demo checklist](demo-checklist.md).

The final header cleanup affects presentation only. In the research workspace,
the large application title/tagline and full-width warning/success banners are
replaced by compact branding, a research title/subtitle, one caution, and a short
source-separation notice. `research_header()` receives `verified=True` only after
`load_research()` succeeds. A failed manifest, snapshot, schema, or receipt check
does not show the verified badge or any research measurements. The badge tooltip
and provenance details distinguish file integrity from scientific approval.
Scientific status stays explicit in **Safety & Scientific Review**; sampling
explanations and study-count caveats are in **Study Context & Limitations**.
Five-language tests cover these disclosures; four added regression cases verify
that a previously visible badge disappears after a local integrity failure.
Desktop and 390-pixel English/German browser checks confirmed no horizontal
overflow. Measurement-card HTML, scale calculations, health charts, source loading,
and storage code were unchanged by this header-only revision.
