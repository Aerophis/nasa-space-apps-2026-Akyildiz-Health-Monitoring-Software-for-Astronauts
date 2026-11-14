# Sprint 2 report — AstroCare AI

## 1. Sprint objectives

AKYILDIZ · 14 November 2026 · Sprint 1 reference: `21108b11299639fa0c3d6210208fd3cf068d28c2`.
P0: validate measurements/records and preserve provenance. P1: fictional manual entry,
local persistence, descriptive personal trends, and understandable data-quality messages.
No diagnosis/treatment, NASA approval, or real-data integration is claimed.
Exact start/end times were not recorded and have not been invented.

This report records the Sprint 2 implementation session before delivery. The English
revision preserves the implementation results below; language-review verification
results are reported separately.

## 2. Planned work

- A/B: classify heart rate and activity while preserving the lead's sleep function.
- C: validate dates, duplicates, types, units, missing/invalid measurements, and provenance.
- D/E: a Streamlit manual-entry form and persistent local storage.
- F/G/H: separate-period comparisons, safe explanations, source/quality visibility, and limited UI fixes.
- Additional tests, real server startup, an attempt to access NASA sources, and Scrum reporting.

## 3. Work actually completed

- `classify_resting_hr()` and `classify_activity_minutes()` were implemented, checking
  None/NaN, non-finite numbers, booleans/text/lists, negatives, and boundaries.
  Heart rate requires a positive finite number; no clinical upper alarm threshold was invented.
- The lead's `classify_sleep_minutes()` code and six tests were preserved unchanged.
  A safe adapter maps the existing `Valid`/`İnvalid` results to shared statuses.
- `validate_health_record()` checks dates, measurement types/units, the fictional profile,
  provenance, and duplicates. Missing and invalid values are distinguished. A record with
  missing fields is accepted if at least one measurement is valid; a record containing
  any invalid measurement is rejected. Missing values are not converted to zero.
- The manual form validates records and shows success/error messages. A successful save
  selects the manual source and refreshes cards, charts, and the table.
- SQLite storage was added. The default `local_data/astrocare.sqlite3` is created on the
  first successful save. Reading alone creates no file. A unique subject/date key rejects
  duplicates atomically; there is no automatic editing or deletion.
- The generated 21-day DEMO-001 series and DEMO-MANUAL-001 records remain separate.
  Both sources are fictional and synthetic; instructions prohibit real health/identifying information.
- Two non-overlapping 7-day periods are compared. Requiring at least 5 comparable
  records per metric in each period is an explicit demo design choice, not a clinical
  threshold. Interpretation is suppressed when data are insufficient; counts and the
  effect of missing data are explained.
- Manual heart-rate values without confirmed resting conditions remain in daily charts
  but are excluded from period comparisons. The confirmation does not validate a real sensor.
- Deterministic non-diagnostic explanations, missing/invalid counts, and embedded chart
  demo/source labels were added. Methodology Markdown indentation was corrected.
  Ollama was not integrated.
- SQLite files and sidecars were excluded from Git; tests use temporary databases.

## 4. Incomplete work

- Direct verification of the complete official Resources list, suitable real NASA file/license/schema
  verification, and application integration could not be completed.
- No new written scientific acceptance closes the **CORRECTIONS REQUIRED** decision.
- Actual sensor quality, sleep start/end timestamps, and exercise plan/type comparisons
  were not implemented; these remain carry-over work outside this session's A–H core tasks.
- Comprehensive usability/accessibility testing and multi-user real health data infrastructure were not implemented.
- Commit/push and Scrum Master closure acceptance remain pending.

## 5. Blockers

- The official Resources URL could not be opened directly; the main challenge page also
  returned 502. A search listing of the challenge title does not verify its Resources list.
- The OSD-575 search record describes serum metabolic panels/cytokines, not the daily
  series for the three metrics. Its dynamic record page returned no readable content;
  file-level licensing was not reverified.
- The lead's sleep function returns differently capitalized labels including a Turkish
  capital İ. Its signature and body were preserved to retain the original learning contribution/tests.

## 6. Solutions

- A shared classification adapter preserves the existing sleep function; new inputs first
  undergo type and finiteness checks.
- SQLite was preferred to CSV because it needs no extra package and provides transactions
  and a unique key. The date span is rechecked under the write lock. Corrupt files are
  neither deleted nor overwritten.
- Dates are normalized to ISO calendar dates. Manual demo dates are limited to 2000–2100,
  with a maximum calendar span of 3660 days for one profile. These are resource-limiting design rules.
- Tests use an environment variable to select temporary databases; local user records were not touched.
- An initial new form test expected three errors but received an additional general validation
  message. It was corrected to check the required field messages rather than the message count.
- Access failures did not block core development; research evidence and concrete follow-up
  work were recorded instead of claiming data integration.

## 7. Team contributions

- Lead / Scrum Master: according to the lead's declaration, author of `classify_sleep_minutes()`
  and the six tests in `tests/test_data.py`. The code/tests were found, and the initial
  29 tests were independently run. Delegation and scope decisions came from the lead.
  New Codex code is not attributed as the lead's handwritten work.
- Codex: with the lead's explicit authorization for the session, A–H integrations, new
  validation/storage/analysis code, UI changes, 75 additional test scenarios, technical
  checks, source-access research, and reporting.
- Muhammed Ali: Python/test support role; no confirmed record of completed individual tasks this sprint.
- Scientific research lead: earlier documents informed the design; no new Sprint 2 review
  or acceptance decision is attributed to this person.

## 8. Test results

- Baseline: **29 passed in 1.47s** (Sprint 1's 23 tests plus the lead's 6 tests).
- Final implementation run: `.\.venv\Scripts\python.exe -m pytest -q` → **104 passed in 2.95s**, 0 failed.
- 75 new parameterized scenarios: None/NaN, negatives/boundaries, types/metadata/units/dates,
  duplicates, missing-versus-zero, the safe sleep adapter, SQLite errors/persistence,
  reading from a separate Python process, records reaching analysis/charts, period coverage,
  form success/error/duplicates, and persistence in a new Streamlit session.
- The previous 29 tests were retained and passed; the lead's six tests were unchanged.
  Test coverage percentage was not measured.
- Imports, `pip check`, and requirements.txt/installed-version consistency passed. No package was installed.
- A real Streamlit server started at 127.0.0.1:8502; health returned 200 / ok and the root page 200.
- The dashboard, source selector, three charts, comparison messages, form, and corrected methodology
  text were observed in the browser. No persistent project record was added through the browser;
  save scenarios were checked with isolated AppTest/SQLite tests.
- Tests did not create the project `local_data` database. The temporary verification server was stopped
  afterward; the user's existing 8501 session was not touched.

## 9. Scientific verification limits

- Scientific status remains **CORRECTIONS REQUIRED**; passing software tests is not clinical validation.
- Recommendations in the local scientific PDF/DOCX informed missing-data, provenance,
  resting-condition, and safe-explanation design. The files were unchanged and not added
  to Git. Not all literature/license claims were reverified.
- General adult sleep guidance was not converted into astronaut clinical alarms. Exercise
  duration is not used to diagnose muscle/bone conditions, nor heart-rate differences to
  diagnose disease/stress. No medication or treatment advice is provided.
- The 5-record rule, 7-day windows, date limits, and manual confirmation box are demo design choices.
- Real NASA data were not used; NASA approval, compliance with the source requirement,
  and clinical suitability are not claimed.

## 10. Work carried into Sprint 3

- [NASA research log](nasa-data-research.md): verify the official Resources source;
  document suitable file fields, access/license, and provenance, then test a separate real-data layer.
  If no suitable source exists, clarify source eligibility with the organizers. Do not relabel OSD-575 as unrelated metrics.
- Obtain a written additional scientific review/acceptance covering open issues and new technical evidence.
- Evaluate measurement protocols/sensor quality, overnight sleep, and exercise plan/type metadata.
- Assess usability/accessibility, local backup, and future schema-versioning needs.
- Real personal data, authorization, and multi-user use require a separate security/privacy design;
  the current version supports fictional use only. Ollama requires separate scope/approval.
- Sprint 3 development was not started in this session.

## 11. GitHub delivery status

- No new commit/push or git add was performed. Sprint 1 history remains intact.
- [Sprint 1 commit](https://github.com/Aerophis/nasa-space-apps-2026-Akyildiz-Health-Monitoring-Software-for-Astronauts/commit/21108b11299639fa0c3d6210208fd3cf068d28c2).
- Original Sprint 2 delivery proposal: `.gitignore`, `app.py`, `astrocare/data.py`, `astrocare/analysis.py`,
  `astrocare/charts.py`, `astrocare/storage.py`, `tests/conftest.py`, `tests/test_data.py`,
  `tests/test_validation.py`, `tests/test_storage.py`, `tests/test_periods.py`,
  `tests/test_sprint2_app.py`, `docs/development.md`, `docs/nasa-data-research.md`, `docs/sprint-2.md`.
- Scientific `docs/research/` files, databases, .venv, caches, and temporary files are excluded.
- At the implementation review, README, requirements.txt, and the Sprint 1 report were unchanged.
  The subsequent English standardization updates README and the Sprint 1 report without rewriting
  Git history; its complete delivery list will be submitted for a new Scrum Master approval.
