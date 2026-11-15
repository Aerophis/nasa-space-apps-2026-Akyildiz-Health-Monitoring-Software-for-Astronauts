# Sprint 4 — Final QA and submission preparation

Implementation date: **14 November 2026**<br>
Final QA and delivery preparation: **15 November 2026**<br>
Team: **AKYILDIZ** · Project: **AstroCare AI**<br>
Baseline: Sprint 3 commit `ddafe06378e4ed126c0393bffefa5a80fc0c078d`<br>
UI status: **Accepted by the team leader / Scrum Master in the current review.**<br>
Delivery status: **Prepared locally; explicit commit, push, and submission approval pending.**<br>
Scientific status: **CORRECTIONS REQUIRED**. No separate scientific acceptance was issued.

## 1. Sprint information and objectives

Finish a readable, professional multilingual dashboard, preserve working health
and research features, validate the accepted interface, and prepare honest English
submission and demonstration material. The final delivery pass must not redesign
the accepted UI or add features. Technical success, UI acceptance, scientific
acceptance, and permission to publish are separate decisions.

## 2. Planned tasks

- Retain the approved navy design, distinct health charts, compact research header,
  and horizontal pre-/post-flight comparison cards.
- Verify health and research workspaces, chart selection, five languages, responsive
  rendering, source separation, missing-file behavior, and dependencies.
- Validate OSD-575 source provenance, pinned checksums, and reproducible acquisition.
- Review all uncommitted changes and public English documentation; protect local
  databases, scientific originals, downloaded data, caches, and secrets.
- Complete this 11-section Scrum report, a submission draft, a 30-second English
  demo storyboard, and an outline of no more than seven presentation slides.
- Present the complete proposed Git file list and wait for explicit approval.

## 3. Completed tasks

### Accepted interface and working behavior

- The final navy palette, readable typography, compact navigation, and expandable
  safety/method/source information are implemented. Sleep uses an area chart,
  resting heart rate a line, and activity bars, with the existing seven-day means.
- **Visible charts** supports any one, two, or three metrics; clearing the selection
  gives guidance. Coverage bars indicate available records, not a medical target.
- English, Turkish, French, German, and Spanish labels and known validation messages
  are available. Locale changes preserve selected metrics, dates, ranges, and sources.
- The research explorer shows authentic Inspiration4 serum data separately from all
  fictional health records. Compact cyan pre-flight and coral post-flight cards
  preserve exact values and units on one shared zero-based scale. Missing results
  are distinct from zero; no intermediate visits, pairing, or continuous line is added.
- The compact header shows **NASA Research Explorer**, **Inspiration4 · Blood serum
  analysis**, and **Verified NASA-hosted data** only after local integrity checks
  succeed. **Research only · Not clinical monitoring** and the source-separation
  notice remain visible. Full limitations and **CORRECTIONS REQUIRED** are accessible.
- Local fictional manual entry, validation, duplicate protection, SQLite storage,
  daily summaries, seven-day means, and period comparisons remain working.

### Final delivery preparation

- Re-ran the full test suite and dependency/import checks; checked both workspaces
  in the actual browser without changing application code or the accepted design.
- Reproduced NASA acquisition into a new ignored QA directory, preserving the
  existing prepared source files and their receipt. Repeated acquisition returned
  the same verified observations.
- Added `docs/research/` to `.gitignore`: these originals were previously untracked
  and excluded by the proposed file list, but lacked an explicit ignore rule.
- Created [submission-draft.md](submission-draft.md), [demo-storyboard.md](demo-storyboard.md),
  and [presentation-outline.md](presentation-outline.md). Updated README links and
  final QA evidence. These are text drafts, not a submitted project, recorded video,
  exported slide deck, or public deployment.

## 4. Incomplete or deferred tasks

- Final commit, push, and competition submission: awaiting explicit approval.
- Demo recording/editing and slide-deck production: plans prepared; not produced.
- Written scientific acceptance and official challenge Resources eligibility
  confirmation: outstanding.
- Independent language review, exhaustive device/screen-reader testing, and full
  accessibility certification: not performed. Framework-owned chrome may remain English.
- Public hosting, authentication, encrypted real-health-data handling, sensor/live
  telemetry integration, record editing/deletion, and AI inference: outside this sprint.

## 5. Blockers

- **Scientific:** the existing review remains CORRECTIONS REQUIRED; technical fixes
  and UI acceptance do not resolve all scientific questions.
- **Eligibility:** no accessible complete official Resources list has established
  this resource's challenge eligibility. NASA hosting alone does not establish it.
- **Delivery:** no authorization to commit, push, or submit has been granted in
  this final-delivery task. All proposed changes remain local.
- The first final-QA test launch was delayed by an automated permission-review
  service usage limit. The requested retry succeeded; it is not an ongoing test
  failure or a judgment that the test command was unsafe.

No critical software defect preventing the local prototype demonstration was
identified in the completed final QA. This is not a declaration of clinical,
security, scientific, or competition eligibility certification.

## 6. Solutions implemented

Earlier Sprint 4 corrections centralized presentation tokens and native control
styling, preserved canonical selections across locale-specific widget identities,
and replaced the rejected research figure with compact cards. Accessible heading
roles avoid unwanted Streamlit heading links/spacing. Escaped source text and
localized missing states preserve an honest research view.

The final delivery pass preserved that accepted implementation. It tightened the
Git exclusion for scientific originals, verified acquisition against the official
NASA file listing/download/metadata endpoints, and prepared the requested English
materials. Changed upstream bytes must stop acquisition for separate review;
checksum pins were not updated or bypassed. Existing files were not deleted or
silently overwritten. No packages were installed.

Earlier local reviews recorded Windows asyncio `WinError 10054` transport callbacks
during reconnection. Those were not application/scientific acceptance evidence.
The new final-QA startup log had no application traceback, and browser and HTTP
checks succeeded. No backend changes were made to address speculative runtime issues.

## 7. Individual team contributions

| Role | Verified contribution / attribution limit |
| --- | --- |
| Team leader / Scrum Master / main developer | Supplied scope, design direction, review feedback, and the current explicit UI acceptance; requested final QA and submission preparation. Delivery approval remains pending. |
| Muhammed Ali — Python development and testing | Role provided by the team leader. No additional verified Sprint 4 work is attributed without evidence. |
| Scientific research teammate — research and validation | Role and earlier review documents identified by the team leader. No new scientific approval or completed Sprint 4 contribution is assumed. |
| Codex — AI development assistance | Implemented the authorized Sprint 4 presentation, localization, regression coverage, and documentation under the lead's direction; performed the final QA and prepared the requested drafts. Codex is a tool, not a human team member. |

The implementation is not represented as entirely hand-written by the team.
Earlier declared personal contributions remain documented in the README and
historical sprint reports. Historical commits and Sprint 1–3 reports are unchanged.

## 8. Test and validation evidence

All commands used the existing project virtual environment on Windows. Final QA
was performed on **15 November 2026**. No application code changed during this pass.

| Check | Final observed result |
| --- | --- |
| Full pytest | **228 passed in 13.83s**, no failures or errors |
| Python / packages | Python 3.11.9; Streamlit 1.67.0; Pandas 3.1.1; Plotly 7.1.0; pytest 9.2.0 |
| Dependency check | `No broken requirements found.` |
| Imports | App, research UI/cards/acquisition, Streamlit, Pandas, Plotly, and pytest imported successfully |
| Streamlit startup | Started from `.venv` on `127.0.0.1:8502`; launcher PID 25376 and Python server child PID 23684 at verification |
| HTTP | Root and `/_stcore/health` returned **200**; health body `ok` |
| Health browser review | Fictional cards and three charts loaded; selected two charts, then restored three; seven-day period comparisons showed counts and non-clinical explanations |
| Five-language browser review | EN → TR → FR → DE → ES → EN; the selected two metrics persisted with translated labels; settled chart count remained two in every locale |
| Research browser review | Verified source badge, 4 participants / 28 samples / 4 analytes, exact C001/Albumin values, original g/dL unit, shared 0–5.7 scale, accessible scientific status, source and checksum details |
| Mobile research review | At 390 px, cards stacked; main client/scroll width 380/380 px, card width 347/347 px; values remained 18 px; no horizontal overflow |
| Browser console | No captured error-level messages in the completed final-QA tab |
| Missing/invalid research | Isolated AppTest cases cover missing files in all five languages; four corruption scenarios withdraw a previously visible verified badge; no synthetic replacement data |
| Original source consistency | All 112 selected observations matched their original CSV sample and column; 80 language/participant/analyte card variants retained values, units, and a common scale |
| Data separation | Authentic records retain `nasa_research` / `is_synthetic=False`; synthetic records retain their demo provenance; health analysis/comparison/charts reject research records and research presentation rejects synthetic records |
| Fresh NASA acquisition | Official endpoints returned the reviewed unrestricted file; 28 samples / 112 observations reproduced in a new ignored QA directory; repeat acquisition was idempotent |
| Git exclusions | Scientific PDF/DOCX, raw research, SQLite and sidecars, virtual environment, caches, logs, and secret-file paths are ignored; none is tracked or proposed for delivery |
| Scientific originals | Both local PDF/DOCX hashes matched the protected pre-existing record |
| Git / documentation | `git diff --check` passed; index empty; HEAD remains the Sprint 3 baseline; English README setup/launch/test commands checked; final drafts reviewed |

Commands for reproduction from the project root:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m astrocare.acquire_research
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8502
```

The review server remains running at [http://localhost:8502](http://localhost:8502).
This is a local development session, not public hosting. Screenshots were captured
from the actual browser outside the repository; they are not fabricated or
claimed as submitted material. Runtime logs and the fresh acquisition evidence
remain under ignored `local_data/`.

Fresh acquisition receipt UTC: `2026-11-15T12:23:01.694633+00:00`, directory
`local_data/final_qa_acquisition_0cb0e89b832c47d98a37aa0932c81a44/`.
CSV: 8,506 bytes; metadata: 493,765 bytes.

- CSV SHA-256: `5eb1e7f025dd8443a9e70111e62bc32afae3432753024489c5c013e401d709d9`
- Metadata SHA-256: `645a0c6693a96cfee62f3af4bc7b4e55365d0eaa8d8756d1d606b2f78f83058c`

Historical Sprint 4 checkpoints, preserved as earlier results rather than final counts:

| Earlier checkpoint | Recorded result |
| --- | --- |
| Sprint 3 baseline | 138 passed in 3.44s |
| Initial Sprint 4 | 142 passed in 3.97s |
| Language/filter correction | 188 passed in 11.38s |
| Readability correction | 208 passed in 24.75s |
| Grouped-column iteration | 212 passed in 22.56s |
| Horizontal-card correction | 224 passed in 15.19s |
| Header cleanup | 228 passed in 15.33s |

These checks are targeted software validation, not a full accessibility, security,
clinical, or scientific certification. Credential-pattern scanning is heuristic;
known credentials were not found in delivery candidates, not proven impossible.

## 9. Scientific review findings

**CORRECTIONS REQUIRED** remains unchanged. See the
[scientific correction matrix](scientific-corrections.md) and
[NASA research log](nasa-data-research.md). No separate documented scientific
acceptance has been issued in this delivery phase.

The three health metrics remain fictional. The separate OSD-575 source comprises
four Inspiration4 commercial crew participants' scheduled serum samples, not live
NASA career astronaut telemetry. Albumin, glucose, sodium, and creatinine are
shown only in their original units; no medical interpretation is added. The CMP
file does not supply daily sleep duration, resting heart rate, or activity minutes.

L− and R+ use distinct launch and return anchors. R+194 appears in the actual
CSV/sample metadata despite the shorter narrative schedule. The small cohort,
missing measurement context, sensor/uncertainty limits, sleep duration versus
quality, and exercise duration versus physiological outcomes remain important.
The shared bar scale is a display extent, never a clinical target or reference range.

The integrity badge confirms local snapshot checks, not NASA endorsement or
scientific approval. No diagnosis, medication advice, clinical risk score,
causal finding, validated flight baseline, operational readiness, or confirmed
challenge Resources compliance is claimed. Linked research gives context, not
clinically validated application thresholds. No AI inference service is integrated.

## 10. Deferred work and next steps

1. Obtain explicit approval for the exact Git delivery list; then separately
   authorize the final commit/push. Do not rewrite Sprint 1–3 history.
2. Have the scientific reviewer assess outstanding corrections and record a written
   decision. Verify the official Resources requirement with an authoritative source.
3. Review the [submission draft](submission-draft.md) for the actual submission form.
4. Rehearse and record the [30-second storyboard](demo-storyboard.md), then create
   a deck from the [seven-slide outline](presentation-outline.md). Neither exists
   as a finished media artifact yet.
5. Consider broader accessibility/device/language review and deployment only as
   separately approved future work. Do not start another development sprint here.

## 11. GitHub delivery status

**No commit, amend, rebase, push, or competition submission was performed.**
The current HEAD remains
[`ddafe06378e4ed126c0393bffefa5a80fc0c078d`](https://github.com/Aerophis/nasa-space-apps-2026-Akyildiz-Health-Monitoring-Software-for-Astronauts/commit/ddafe06378e4ed126c0393bffefa5a80fc0c078d).
The index is empty. UI acceptance is recorded; publication approval is pending.

Proposed delivery: **22 files**. Paths below are explicit and relative to the
repository root. Only these files should be staged after approval; never use
`git add .`. No Sprint 4 commit link exists yet.

| # | Path | Git state |
| --- | --- | --- |
| 1 | `.gitignore` | Modified; adds protection for local scientific originals |
| 2 | `.streamlit/config.toml` | New |
| 3 | `README.md` | Modified |
| 4 | `app.py` | Modified |
| 5 | `astrocare/charts.py` | Modified |
| 6 | `astrocare/i18n.py` | New |
| 7 | `astrocare/research.py` | Modified |
| 8 | `astrocare/research_cards.py` | New |
| 9 | `astrocare/research_ui.py` | Modified |
| 10 | `astrocare/theme.py` | New |
| 11 | `astrocare/ui.py` | New |
| 12 | `docs/development.md` | Modified |
| 13 | `docs/demo-checklist.md` | New |
| 14 | `docs/sprint-4.md` | New |
| 15 | `docs/submission-draft.md` | New |
| 16 | `docs/demo-storyboard.md` | New |
| 17 | `docs/presentation-outline.md` | New |
| 18 | `tests/test_analysis.py` | Modified |
| 19 | `tests/test_i18n.py` | New |
| 20 | `tests/test_presentation.py` | New |
| 21 | `tests/test_readability.py` | New |
| 22 | `tests/test_research.py` | Modified |

The previous proposed list contained 18 files. This final pass adds `.gitignore`
and the three new submission/demo/presentation drafts. There are 9 modified and
13 new proposed files. Scientific PDF/DOCX files under `docs/research/` now remain
local and ignored, along with SQLite, raw research, virtual environments, caches,
logs, and secret-file paths. Dependency pins and historical Sprint 1–3 files and
commits are unchanged. A non-clean working tree is expected until authorized delivery.
