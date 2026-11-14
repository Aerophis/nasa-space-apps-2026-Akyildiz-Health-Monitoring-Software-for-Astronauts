# Sprint 1 closure report — AstroCare AI

## 1. Sprint information and objectives

- Team: AKYILDIZ · Sprint: 1 / 4 · Date: 14 November 2026.
- Event: NASA Space Apps Challenge 2026.
- Challenge: Create Health Monitoring Software for Astronauts on Space Missions.
- Scrum Master / team lead / lead developer: the user.
- Objective: the first working prototype for monitoring three health-related metrics with synthetic data, without diagnosis or treatment advice.
- Status at the original review: technical checks passed; scientific status CORRECTIONS REQUIRED; the report and GitHub delivery awaited Scrum Master approval.
- Exact sprint times were not recorded. The report follows the 11 headings supplied by the Scrum Master; a separate format specification from the Niğde organizers had not been provided.

This is the historical pre-delivery review record. Pending-approval statements below
refer to that review, not the current repository state. The English revision preserves
the original accomplishments, test results, and unresolved issues.

## 2. Planned work

- Reproducible demo data; separate data, analysis, and chart modules; a Streamlit dashboard.
- Daily changes, 7-day averages, valid observation counts, and missing/invalid data checks.
- Automated tests, startup checks, a basic UI review, and scientific research.
- Planned responsibilities: coordination/integration by the lead; Python/test support by Muhammed Ali; literature review and evaluation by the scientific research lead. Assignments are not evidence of completed individual contributions.

## 3. Work actually completed

- An AI-assisted Streamlit/Pandas/Plotly prototype: a fictional profile, 21 days of fixed-seed data, three summary cards, three interactive charts, date/range selection, and a daily table.
- Previous-calendar-day changes, 7-day averages, and valid measurement counts; missing values are not counted as zero.
- The DEMO — SIMULATED DATA label, a statement that the product is not NASA-approved, and statements that it does not provide diagnoses or medication advice.
- The `sleep_hours` conversion in `analyze_daily()`, reported as written by the lead, and its two tests were verified in the files. The minutes column and missing values are preserved.
- The code/test structure and local development guide were prepared; 23 tests were independently rerun.
- The lead reported a basic UI review, and a screenshot was shared in the chat; this was not treated as comprehensive usability testing.
- The existence and contents of two scientific documents were verified during closure; scientific acceptance of the application was not considered complete.

## 4. Incomplete or deferred work

- Written closure of scientific corrections and an additional application acceptance record from the scientific research lead.
- Definitive verification of the official NASA Resources list and integration of suitable real data.
- Measurement conditions/sensor quality, a personal baseline, and planned-versus-completed exercise comparisons.
- Detailed usability testing and UI improvements.
- Confirmation of Muhammed Ali's completed individual tasks; approval for the Sprint 1 commit/push.

## 5. Problems and blockers

- A relative application path in the initial UI test; restricted local socket access in the terminal.
- The lead's terminal could not resolve the relative Python path; its working directory at the time was not definitively recorded.
- The scientific PDF had been prepared without reviewing code, screenshots, or test outputs; the document explicitly states this limitation.
- Some DOCX status notes described the synthetic demo as not yet created; those notes were no longer current for the working prototype.
- No written additional scientific acceptance, independent Scrum format specification, or official Resources confirmation was available. At that review, the README contained only the repository title.

## 6. Solutions applied

- The UI test path was corrected; local connection checks were run with the necessary permission; navigation to the project directory was explained.
- The PDF was parsed with `pypdf` and the DOCX with `python-docx` using bundled document tools. The files were not read as plain text, source documents were not modified, and no project package was installed.
- PDF pages 1 and 8 were also viewed. The DOCX content was reviewed; no page-layout or visual-quality approval was given.
- The evidence limitations at the document's preparation date were distinguished from the later technical test results; the scientific decision was not changed.
- Only this report was edited during closure. Python code, tests, README, .gitignore, and requirements.txt were unchanged; no feature was added.

## 7. Individual team contributions

| Person / support | Recorded contribution and evidence limits |
| --- | --- |
| Team lead / Scrum Master / lead developer | Planning, Codex direction, scientific coordination, and UI review are based on the lead's declaration. The sleep_hours calculation and two tests attributed to the lead were present and rerun; individual authorship is attributed according to that declaration. |
| Muhammed Ali | Python/test support role; no detailed verified record of completed individual tasks. Contributions await confirmation. |
| Scientific research lead — pharmacy student and the lead's cousin | According to the lead: research/report preparation, measurement and source/license review, joint evaluation, and Sprint 2 recommendations. The two documents and their scientific contents were reviewed; individual authorship and joint meeting details were not independently verified. |
| Codex — AI assistance | Initial prototype and original 21 tests, technical verification, document review, and reporting support. The complete prototype is not presented as code written by hand by the lead. |

## 8. Test and verification results

- Final independent run at closure: `.\.venv\Scripts\python.exe -m pytest -q` → **23 passed in 1.47s**.
- An earlier closure run took 1.52s; the lead reported a previous run of 1.44s. These are separate runs.
- `test_sleep_minutes_to_hours`: 450 minutes → 7.5 hours; `test_missing_sleep_data`: None → NaN, without conversion to zero.
- Other tests cover data generation, calendar gaps, invalid/duplicate records, changes/averages, chart series, and UI date/range controls. Test coverage percentage was not measured.
- Application imports and `pip check` passed. An earlier audit verified that requirements.txt matched installed versions.
- Python 3.11.9; Streamlit 1.67.0; Pandas 3.1.1; Plotly 7.1.0; pytest 9.2.0.
- A temporary 127.0.0.1:8502 server was restarted: health 200 / ok, root page 200. It was stopped afterward; the existing 8501 session was not touched.
- .gitignore excludes the environment, caches, local secrets, and temporary files. The proposed delivery excludes scientific documents. Basic secret/large-file checks are not an absolute guarantee.
- Passing technical tests does not replace clinical validation or scientific acceptance.

## 9. Scientific review outcome and open issues

Local documents reviewed, excluded from GitHub delivery:

- `docs/research/AKYILDIZ_Sprint1_Bilimsel_Dogrulama_Raporu.pdf`: 8 pages; the decision on pages 1 and 8 is **CORRECTIONS REQUIRED**.
- `docs/research/AstroCare_Bilimsel_Arastirma_Duzeltilmis.docx`: scientific research, measurement limitations, a source/license matrix, and NASA data source evaluation.

The separate `AstroCare_Bilimsel_Arastirma_Duzeltilmis.pdf` was not present in this directory and was not considered reviewed.

The PDF conditionally supports the descriptive trend design but states that application
code, screens, and tests had not been reviewed when it was prepared. Some of those
items were independently verified technically during closure; this is not a new
acceptance record from the scientific research lead. The lead reported an additional
joint review, but no written closure exists. **CORRECTIONS REQUIRED remains the decision.**

| Scientific recommendation | Current technical evidence / open work at the Sprint 1 review |
| --- | --- |
| Do not count missing measurements as zero; show valid counts | Verified in code and tests; explanatory low-coverage notifications remain open. |
| Synthetic provenance and limits on clinical claims | A general demo label and source fields exist; detailed per-chart/statistic provenance/quality is partial. |
| Day definition and 7-day window | UTC calendar days, averages, and counts exist; no overnight sleep calculation from start/end timestamps. |
| Comparable resting-heart-rate conditions | Only a synthetic series exists; resting-condition/sensor-quality metadata and a personal baseline are absent. |
| Planned/completed exercise and type | Duration only; no plan/type comparison. Exercise duration is not used to diagnose muscle/bone conditions. |
| NASA data and license traceability | No real data download/processing/integration; source and file-level suitability remain unresolved. |

The documents' sleep guidance, heart-rate conditions, and exercise limitations were
not converted into clinical alarm or diagnostic rules. DOCX notes describing an
uncreated demo reflect the evidence available to that document; the working prototype
at closure is recorded in sections 3 and 8.

The documents evaluate OSD-575 as serum chemistry rather than a daily series for the
three metrics. They state that the complete official Resources list could not be
verified and that a secondary list does not establish definitive eligibility. Not all
external sources or license claims were reverified during closure. **Neither NASA
data integration nor compliance with the Resources requirement is claimed.** Permission
to redistribute the scientific documents was not confirmed; they will not be added to GitHub.

## 10. Work carried into Sprint 2

The Scrum Master's priority order; implementation had not started at this closure review:

1. Improve the display of data provenance and measurement quality.
2. Extend missing, duplicate, and invalid measurement checks.
3. Allow users to enter new health records.
4. Compare measurements with personal baseline values.
5. Provide source-based, non-diagnostic explanatory messages and written tracking of scientific corrections.
6. Compare planned/completed exercise and exercise types.
7. Definitively verify the official NASA Resources list — open, high-priority research work.
8. Actually use a suitable NASA data source after verifying source/license/field suitability — open, high-priority integration work.
9. Improve the UI and review the Markdown/display issue in the methodology area.

Ollama will be considered later only if time and technical suitability allow. Future
Python tasks will identify the filename, full path, function, location, task, expected
result, test, and VS Code Explorer path; hints will precede the lead's own coding work.

## 11. GitHub commit and evidence links

- [Repository](https://github.com/Aerophis/nasa-space-apps-2026-Akyildiz-Health-Monitoring-Software-for-Astronauts).
- [13feb3b environment preparation](https://github.com/Aerophis/nasa-space-apps-2026-Akyildiz-Health-Monitoring-Software-for-Astronauts/commit/13feb3bf71c91892d48266dd3293cf1915533f9c): pre-event environment preparation; not a Sprint 1 application development commit.
- Local evidence at review: [analysis](../astrocare/analysis.py), [lead's tests](../tests/test_sleep_hours.py), [data/chart tests](../tests/test_analysis.py), [UI test](../tests/test_app.py), [development guide](development.md). These were not yet remote Sprint 1 evidence at that review.
- At this historical review, the Sprint 1 commit/push had not been performed; a new commit link was to be recorded after approval and delivery. Terminal outputs were in the chat and were not saved as separate files.
- Proposed delivery at review: `app.py`, `astrocare/__init__.py`, `astrocare/data.py`, `astrocare/analysis.py`, `astrocare/charts.py`, `tests/test_analysis.py`, `tests/test_app.py`, `tests/test_sleep_hours.py`, `docs/development.md`, `docs/sprint-1.md`.
- No files beyond those 10 were to be added. Scientific PDF/DOCX files, .venv, caches, secrets, and temporary files were excluded. `docs/research/` was to remain untracked locally; bulk `git add .` was not to be used.
- The index was empty and commit/push awaited Scrum Master approval. README, .gitignore, and requirements.txt were unchanged. A short README setup summary was only a recommendation.
