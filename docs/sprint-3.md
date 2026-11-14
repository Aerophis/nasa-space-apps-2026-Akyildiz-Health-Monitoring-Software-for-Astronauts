# Sprint 3 report — AstroCare AI

## 1. Sprint information and objectives

- Team: AKYILDIZ · Event: NASA Space Apps Challenge 2026 · Date: 14 November 2026.
- Challenge: Create Health Monitoring Software for Astronauts on Space Missions.
- Scrum Master / lead developer: the team lead (user).
- Baseline: main at `f52ac99f8695f9bac95d226db18a7c9fa9ffa87c`; 104 passing tests.
- Goal: a small reproducible genuine NASA research integration, scientific transparency,
  source-backed explanations, and preservation of the synthetic/SQLite dashboard.
- Status: implementation and technical verification completed; the Scrum Master reviewed the
  application in the browser and approved general functionality and technical delivery.
  Scientific status remains **CORRECTIONS REQUIRED**; technical delivery approval is not scientific acceptance.
- Exact sprint start/end times were not recorded. Planning deadline supplied by the Scrum Master:
  15 November 2026 at 23:59 local time. No independent deadline certification is implied.

## 2. Planned tasks

- A: verify official Resources and consult HRP, OSDR, OSD-575, NLSP, and discussion #2025.
- B: obtain and inspect a genuine accessible research file; integrate separately from demo telemetry.
- C: audit the local scientific documents and implement feasible non-clinical corrections.
- D/E: deterministic evidence categories, source links, limitations, and separate UI provenance labels.
- F: consider optional local AI only if it does not threaten delivery; retain deterministic operation.
- Preserve baseline features, add tests, document reproducibility, prepare closure evidence,
  and leave a verified local server running for review without committing/pushing.

## 3. Completed tasks

- Used the official NASA-documented file and study metadata APIs to obtain OSD-575 version 3 metadata
  and the unrestricted `LSDS-8_Comprehensive_Metabolic_Panel_CMP_TRANSFORMED.csv`.
- Verified actual CSV shape (28 samples × 58 columns), file size (8,506 bytes), original field names,
  units, four published subject pseudonyms, sample metadata, and pre-/post-flight contexts.
- Recorded source URL, filename, DOI, license evidence, SHA-256 pins and actual UTC acquisition receipt.
  Official indexed study text lists CC0-1.0; the file API lists this CSV as unrestricted.
- Built a separate offline NASA Research Data Explorer selecting albumin, glucose, sodium,
  and creatinine: 112 observations in original units. All 112 values were independently matched
  against the exact original CSV column/sample. Example: C001_serum_L-3 albumin = 4.9 g/dL.
- Preserved L-92, L-44, L-3 and R+1, R+45, R+82, R+194 sample visits. L and R retain distinct
  launch/return anchors; markers do not imply a continuous calendar or daily telemetry.
- Disclosed the narrative study summary's shorter schedule versus the actual R+194 CSV/metadata records.
- Reproducible acquisition and strict offline loading reject missing, changed, malformed or restricted
  data rather than manufacturing a replacement. The app itself does not fetch research files.
- Kept generated telemetry, manual demo records, and authentic research data in separate paths/workspaces.
  Health analysis, period comparisons, and chart boundaries reject incompatible research provenance.
- Added deterministic source-backed context cards separating observed fictional measurements,
  calculated trends, prototype design choices, NASA research context, and interpretation limits.
- Suppressed manual daily bpm deltas unless both consecutive records declare resting conditions.
  Existing period comparisons already filter unconfirmed resting records.
- Clarified numeric completeness versus sensor validation; labeled duration-versus-quality and
  activity-versus-muscle/bone interpretation limits. Created a scientific correction matrix.
- Preserved the 21-day generated demo, manual form, SQLite schema/persistence, duplicate protection,
  the lead's sleep classifier, existing tests, historical sprint reports, and prior commits.
- Launched the updated app persistently at **http://localhost:8501** for the Scrum Master's browser review.

## 4. Incomplete or deferred tasks

- Full direct verification of the official challenge Resources list and resource-eligibility confirmation.
- New written scientific acceptance closing the prior CORRECTIONS REQUIRED decision.
- Actual sensor calibration/signal-quality assessment, validated personal flight baselines, sleep quality
  or overnight start/end calculations, and planned-versus-completed exercise/type tracking.
- Comprehensive usability/accessibility evaluation and multi-user real personal-health data handling.
- The Scrum Master's UI/UX findings are non-blocking for Sprint 3 and are deferred to Sprint 4:
  excessive visible explanation text, small text, similar-looking charts, and research-data presentation.
  No UI changes were made during this delivery review; sources, provenance and safety notices remain intact.
- Additional immune/cytokine assays were not downloaded or integrated. Only the reviewed CMP subset is used.
- Optional Ollama integration was skipped to protect delivery time and avoid unsupported generated
  health/citation content. No model download or new service dependency was introduced.
- The Scrum Master authorized the specified 18-file commit and push, subject to final technical checks.
  Sprint 4 development/presentation work did not start.

## 5. Blockers

- The official Resources request failed in the browsing tool; no complete list was recovered.
- Dynamic OSD-575/NLSP pages did not expose readable lines. A direct OSDR root request redirected
  to the NASA BPS data portal; this was not treated as a dataset integration.
- Restricted-terminal DNS initially failed for NASA API requests; permission-enabled requests succeeded.
- The study metadata API does not contain a license field; license evidence was recovered from the official
  indexed study record, with the API's unrestricted flag recorded separately.
- The actual file/sample table includes R+194 while the study narrative describes fewer post-flight visits.

## 6. Solutions implemented

- Followed official NASA API documentation instead of relying on the dynamic UI or third-party dataset copies.
- Chose a small reviewed assay file and four explicit analyte/unit mappings. Reference-range and
  demographic/race-based derived columns are not interpreted or displayed.
- Added a measurement-free public manifest and an explicit acquisition module. Raw research files, full
  metadata, receipt and inspection files stay ignored under `research_data/`; originals are not overwritten.
- Used metadata to validate species/material, subject/sample identity, phase, units and sampling anchors;
  pinned both CSV and metadata bytes. Unknown upstream changes require review rather than silent acceptance.
- Added honest source-information fallback states when numerical loading fails. A source link alone is
  not described as numerical integration.
- Documented the scientific correction status per finding; technical checks do not override reviewer authority.
- Checked 8501/8502 before launch: no listeners. Started the project virtual-environment Streamlit server
  in a hidden persistent process on 127.0.0.1:8501, with logs in ignored local_data. It was deliberately not stopped.

## 7. Individual team contributions

- Team lead / Scrum Master: authorized and scoped Sprint 3, including real research exploration and the
  persistent local review server. No new handwritten Python contribution is attributed without evidence.
  Prior declared sleep calculation/classifier and tests remain credited in historical reports.
  Subsequently reviewed the NASA Research Data Explorer in the browser, accepted its general functionality,
  and identified non-blocking UI/UX improvements for Sprint 4.
- Codex: AI-assisted source/API investigation, actual acquisition, parsing/validation, UI integration,
  deterministic context, tests, documentation, server verification and closure reporting under explicit authorization.
- Scientific research role (the lead's cousin): original research and the Sprint 1 scientific review remain
  attributed to this role. The documents informed the audit; no new Sprint 3 reviewer decision is invented.
- Muhammed Ali: Python/test support role; no newly confirmed individual Sprint 3 work recorded.

## 8. Test and validation evidence

- Baseline: all existing **104 tests passed** before development.
- Final full suite: `.\.venv\Scripts\python.exe -m pytest -q` → **138 passed in 3.50s**, 0 failures.
  The previous 104 tests remain; 34 additional cases cover parser/provenance/unit/context errors,
  offline loading, missing/tampered files, acquisition failures, source-linked explanations and UI behavior.
- Pre-delivery rerun after Scrum Master review: **138 passed in 3.54s**, 0 failures; `pip check` passed.
- Unit parser fixtures contain explicitly artificial test inputs only; they are not source measurements or app fallbacks.
- Separate actual-file check with network requests disabled: all **112 selected values** exactly matched
  original CSV samples/columns. Actual-data AppTest displayed seven C001 albumin visits, first sorted
  sample L-92 = 5.0 g/dL. Numerical equality is not a clinical assessment.
- Import checks, `pip check`, and requirements.txt/installed dependency consistency passed. No package installed.
- Persistent Streamlit server: localhost:8501 root **200**, health **200 / ok**. Browser verification showed
  the updated Sprint 3 health panel and real NASA explorer with study/license/context, analyte selection,
  scheduled sample markers and original units. The server remains running for review.
- Scientific PDF/DOCX SHA-256 values matched the pre-development snapshots. No scientific document was modified.
- Git exclusion checks confirmed research_data, local_data/logs, SQLite sidecars, .venv and caches are ignored.
  No local personal health entry was created. Full Git/diff/secret checks are part of the delivery review.

## 9. Scientific review findings

Overall scientific status: **CORRECTIONS REQUIRED**. No NASA approval, clinical validation,
flight readiness, medical diagnosis, medication/therapy recommendation or causal correlation is claimed.

See [scientific correction matrix](scientific-corrections.md) for the required classifications:
Implemented and tested; Partially implemented; Open / not implemented; Requires scientific reviewer approval.

Implemented technical evidence includes missing-versus-zero handling, completeness counts, discrete
research context, provenance boundaries, original units, safe source-backed explanations and clear
prototype rules. Resting-condition verification and personal baselines remain partial; actual sensor
quality, sleep quality and exercise-plan semantics remain open. A new scientific reviewer acceptance
is required even though the genuine NASA-hosted CMP file is now numerically integrated locally.

The research cohort comprises Inspiration4 commercial crew serum samples, not NASA career astronaut
continuous health telemetry. No CMP value is relabeled as sleep, resting bpm or exercise minutes.

## 10. Sprint 4 backlog

1. Obtain official Resources/organizer confirmation of source eligibility and written scientific review
   of the correction matrix and research explorer.
2. Final QA on a fresh checkout: acquire once, verify checksums, disconnect network, check the research view,
   and confirm honest behavior if files are missing. Keep the synthetic/manual workflows intact.
3. Review exact Git list, attribution/license notes, AI disclosure and English content; exclude all local
   participant files, scientific documents, databases, secrets and logs from delivery.
4. After Sprint 3 review, prioritize demo recording, English presentation, final GitHub review, project
   submission and local organizer requirements within the Scrum Master's stated deadline.
5. Do not add Ollama or broad new clinical/data features at the expense of final delivery. No Sprint 4 implementation here.

### UI/UX priorities from the Scrum Master's browser review

These improvements do not block Sprint 3 delivery and have not been implemented in this review:

- A more modern, professional dashboard design.
- Less always-visible text, with expandable scientific explanations.
- More readable fonts and clearer headings.
- Greater chart variety and stronger data visualization.
- Understandable summary cards for NASA research findings, without clinical overinterpretation.
- Reduced unnecessary page length.
- A clean presentation suitable for an English-language demo video.

Scientific sources, data provenance and safety notices must remain accessible; reducing visible
text must not remove them. Prioritize these presentation improvements alongside the final QA
and submission tasks above. Sprint 4 development has not started.

## 11. GitHub delivery status

- Pre-commit HEAD: [Sprint 2 f52ac99](https://github.com/Aerophis/nasa-space-apps-2026-Akyildiz-Health-Monitoring-Software-for-Astronauts/commit/f52ac99f8695f9bac95d226db18a7c9fa9ffa87c).
- The Scrum Master approved the exact 18-file delivery and requested the message
  `feat: integrate NASA OSD-575 research data and scientific evidence`.
  This report accompanies that authorized delivery; the resulting commit URL will be reported after push.
  Sprint 1/2 commits must remain unchanged; no amend, rebase or history replacement is authorized.
- Modified delivery candidates: `.gitignore`, `README.md`, `app.py`, `astrocare/analysis.py`,
  `astrocare/charts.py`, `docs/development.md`, `docs/nasa-data-research.md`, `tests/conftest.py`.
- New delivery candidates: `astrocare/acquire_research.py`, `astrocare/research.py`,
  `astrocare/research_ui.py`, `astrocare/science.py`, `data/osd575_manifest.json`,
  `docs/scientific-corrections.md`, `docs/sprint-3.md`, `tests/test_research.py`,
  `tests/test_science.py`, `tests/test_sprint3_app.py`.
- Total proposed delivery: **18 files**. The manifest contains schema/source metadata, not participant measurements.
  Raw CSV/full metadata and acquisition records remain local and ignored; scientific docs remain untracked and excluded.
- Final checks must confirm the approved file list, complete test suite, provenance separation and
  source/checksum consistency before commit/push. No Sprint 4 feature work is part of this delivery.
