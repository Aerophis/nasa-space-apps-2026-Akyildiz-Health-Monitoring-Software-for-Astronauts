# Scientific correction matrix — Sprint 3

Date: 14 November 2026. Review input: the local Sprint 1 scientific validation PDF
and corrected DOCX, attributed to the scientific research role by the team lead.
The originals were parsed for relevant recommendations and remain unchanged and
outside the proposed Git delivery. This matrix is a software implementation audit,
not a new decision by the scientific reviewer. Overall status: **CORRECTIONS REQUIRED**.

| Finding | Status | Implementation/evidence | Remaining limit |
| --- | --- | --- | --- |
| Missing values versus actual zeros | Implemented and tested | Existing validation/SQLite tests and new explanation tests preserve missing, invalid, and actual zero separately. | Missing data cannot be interpreted as lack of exercise or sleep. |
| Completeness and valid measurement counts | Implemented and tested | Daily/7-day counts, period coverage, and selected research sample counts are shown. Missing research values stay missing. | Numeric validity is not sensor quality. |
| Individual baseline versus comparison periods | Partially implemented | Non-overlapping seven-day windows and minimum comparable counts are tested. | A rolling prototype baseline is not a scientifically validated personal flight baseline; contextual factors are incomplete. |
| Resting-state limitations | Partially implemented | Manual daily bpm deltas now require both consecutive records to declare resting conditions; period comparisons already filter unconfirmed rest states. | Manual confirmation is not objective measurement verification; posture/time/medication/context are not captured. |
| Sensor quality and uncertainty | Open / not implemented | Explanations explicitly disclose unverified device calibration, signal quality and measurement context. | No real sensor integration, calibration model, or uncertainty estimate. |
| Sleep duration versus quality | Implemented and tested | Source-linked sleep card explicitly states that duration does not measure quality/circadian alignment or diagnose a disorder. | No sleep-quality instrument or overnight timestamp calculation. |
| Exercise duration versus physiological diagnosis | Implemented and tested | Source-linked activity card limits interpretation; no muscle/bone disease inference or treatment advice. | Exercise intensity/type and planned-versus-completed sessions remain open. |
| Synthetic versus authentic research provenance | Implemented and tested | Separate workspaces; checksummed OSD-575 snapshots; source labels; incompatible data rejected by health analysis/chart boundaries. | No association or correlation with fictional subjects is supported. |
| Units, source and measurement context | Implemented and tested | Four explicit original-column/unit mappings; sample metadata matches; study/DOI/license/receipt/checksum shown. Research markers are discrete biospecimen visits. | Only the four reviewed CMP analytes are exposed. Study summary/CSV R+194 discrepancy is disclosed. |
| Clinically unvalidated prototype rules | Implemented and tested | Five-observation/seven-day rules and numeric bounds remain labeled design/data-format choices, not clinical alarms. | Their scientific/operational suitability requires separate review. |
| Published findings versus calculated trends | Implemented and tested | Context cards separate observed fictional data, calculations, design rules, NASA source links, and limitations. | Short background summaries are not a clinical protocol. |
| Official Resources requirement | Open / not implemented | Direct list access failed; discussion guidance is documented separately from rules. | Organizer/official confirmation still required even though a real NASA-hosted file is now used. |
| Overall scientific acceptance | Requires scientific reviewer approval | Code/tests and the actual-file verification provide new evidence for review. | No reviewer approval, NASA endorsement, clinical validation, or flight readiness is claimed. |

## Evidence and attribution

- Parser/provenance/offline tests: `tests/test_research.py`.
- Deterministic source/limitation checks: `tests/test_science.py`.
- Workspace fallback and resting-condition UI checks: `tests/test_sprint3_app.py`.
- Actual downloaded-file comparison: all 112 selected values were matched to original columns/samples,
  separately from artificial unit-test fixtures. See the NASA research log.
- Existing Sprint 1/2 tests remain in the suite; no source PDF/DOCX is redistributed.
- Codex implemented this matrix and the technical changes under the lead's authorization.
  Scientific research and the original review remain attributed to the scientific research role;
  no new team-member review or contribution is invented.

The next scientific reviewer should assess the remaining limits and record a written
acceptance/correction decision. This document does not change **CORRECTIONS REQUIRED**.
