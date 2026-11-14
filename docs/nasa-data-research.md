# NASA data research — Sprint 3

Review date: 14 November 2026. A genuine NASA-hosted OSD-575 CMP file has been
downloaded, processed, and integrated locally in a separate offline research explorer.
The sleep/resting-heart-rate/activity dashboard remains entirely synthetic.
This supersedes Sprint 2's unresolved numerical-integration status without changing
historical Sprint 1/2 reports or Git commits.

## Official resources and access evidence

| Resource | Verified result in this session | Limit |
| --- | --- | --- |
| [Official challenge Resources](https://www.spaceappschallenge.org/2026/challenges/health-monitoring-software/?tab=resources) | Direct browsing request failed; the complete list was not retrieved. | Official Resources membership and competition eligibility are not certified. |
| [NASA Human Research Program](https://www.nasa.gov/hrp/) | Official research/program page accessible. | Scientific background, not a downloadable unified telemetry dataset. |
| [NASA OSDR entry point](https://osdr.nasa.gov/) | Redirected to the [NASA BPS data page](https://science.nasa.gov/biological-physical/data/). The documented OSDR file and metadata APIs returned study data. | A portal is not an integration by itself. |
| [OSD-575 study](https://osdr.nasa.gov/bio/repo/data/studies/OSD-575) | Dynamic page has no readable lines in direct browsing; official indexed study text identifies version 3, title, DOI, and License: CC0-1.0. Actual NASA APIs and file download succeeded. | License evidence is the official indexed study record, not a license field in the metadata API. |
| [NASA Life Sciences Portal](https://nlsp.nasa.gov/) | Landing page returned no readable content in the browsing tool. | No downloadable suitable file, license, or human-health series was verified there. |
| [NASA Space Apps discussion #2025](https://github.com/nasa/spaceapps/discussions/2025) | Navigator response was readable; distinguishes research datasets from simulated telemetry and discusses repository access. | Guidance, not a replacement for official challenge rules or Resources verification. |

API access was discovered through the official [NASA API documentation](https://api.nasa.gov/)
and [OSDR API documentation](https://visualization.osdr.nasa.gov/biodata/api/).
The first restricted-terminal request failed DNS resolution; the permission-enabled
request to the same official endpoints succeeded. No credentials were used.

## Candidate evaluation

| Candidate | Official title / source | Origin and actual measurements | Access and license | Downloaded / processed / integrated |
| --- | --- | --- | --- | --- |
| OSD-575 CMP | SpaceX Inspiration4 Blood Serum Metabolic Panel and Immune/Cardiac Cytokine Arrays (Comprehensive Metabolic Panel and Multiplex); NASA OSDR; DOI 10.26030/mc5d-p710 | Human serum; four commercial Inspiration4 crew participants. Laboratory CMP measurements at scheduled pre-/post-flight visits, not continuous NASA career astronaut telemetry. | Selected CMP CSV listed `restricted=false`. Official indexed study record lists CC0-1.0. | Yes / yes / yes locally, in the separate explorer. Four analytes only. |
| OSD-575 immune/cardiac cytokine files | Same study; additional assay files listed in the official file API | Human serum immunoassay measurements; distinct from the CMP assay and from daily health telemetry | Listed as unrestricted in the study file API; study CC0-1.0 label does not remove the need to check any other selected file. | No / no / no. Not required for the small Sprint 3 integration. |
| NLSP / LSDA candidate search | NASA Life Sciences Portal | Human spaceflight/ground-analog research catalogue; no specific suitable file verified in this session | Record-level access and license unresolved; no open daily dataset assumed | No / no / no. |
| HRP background pages | NASA Human Research Program and the three context-card sources below | Scientific/program information, not an animal/environmental/human numerical file selected for loading | Public links and original short summaries; no images/article PDFs redistributed | Pages consulted; no numerical dataset downloaded or integrated from these pages. |

No animal or environmental dataset was substituted for human serum or the three demo metrics.
No participant identity lookup or association with fictional profiles was attempted.

## Actual file and reproducibility evidence

- Official file listing: https://osdr.nasa.gov/osdr/data/osd/files/575
- Official metadata: https://osdr.nasa.gov/osdr/data/osd/meta/575
- File: `LSDS-8_Comprehensive_Metabolic_Panel_CMP_TRANSFORMED.csv`
- Original URL: https://osdr.nasa.gov/geode-py/ws/studies/OSD-575/download?source=datamanager&file=LSDS-8_Comprehensive_Metabolic_Panel_CMP_TRANSFORMED.csv
- Retrieved/verified on 14 November 2026; exact UTC acquisition time is in the local `receipt.json`.
- Raw size: 8,506 bytes; UTF-8 with BOM; 28 sample rows × 58 original columns.
- CSV SHA-256: `5eb1e7f025dd8443a9e70111e62bc32afae3432753024489c5c013e401d709d9`.
- Metadata snapshot size: 493,765 bytes; SHA-256: `645a0c6693a96cfee62f3af4bc7b4e55365d0eaa8d8756d1d606b2f78f83058c`.
- Metadata snapshot: OSD-575 version 3; 28 corresponding sample records; Homo sapiens / Serum.
- Checked sample context: L-92, L-44, L-3 (before launch); R+1, R+45, R+82, R+194 (after return).
  L and R use different anchors; no calendar dates or continuous flight-day series were invented.
- The narrative study summary omits R+194. It is explicitly present in the actual CSV and
  sample metadata, so the explorer retains it with this limitation disclosed.

The [manifest](../data/osd575_manifest.json) records all original columns, selected
analyte/unit mappings, URLs, licensing evidence, and integrity pins. The application
selects albumin (g/dL), glucose (mg/dL), sodium (mmol/L), and creatinine (mg/dL):
112 long-form observations from 28 biospecimens. Reference-range and demographic/race-based
derived columns are not interpreted. The source has no daily sleep/bpm/exercise fields.

Offline proof compared all 112 selected values with the original CSV's exact column
and sample. Example checks: C001_serum_L-3 albumin is 4.9 g/dL; the chronologically
first displayed C001 albumin sample, L-92, is 5.0 g/dL. These are source measurements,
not normal-range statements or diagnoses. A separate actual-data AppTest loaded seven
sample rows for that selected participant/analyte with network access disabled.

## Acquisition and redistribution decision

Run explicitly, once with network access:

```powershell
.\.venv\Scripts\python.exe -m astrocare.acquire_research
```

The app does not automatically download anything. Prepared local snapshots and the
acquisition receipt support offline loading. Changed checksums, units, sample context,
missing files, and parsing errors stop numerical display; no simulated fallback exists.
The checked file is publicly available and the study lists CC0-1.0, but this delivery
still prefers reproducible acquisition over redistributing participant measurements.
Raw CSV, full metadata, listing, and receipt remain ignored under `research_data/`.
Only code, the measurement-free manifest, tests, and documentation are proposed for Git.
Original scientific PDF/DOCX documents remain unmodified and excluded.

## Scientific context sources

- [NASA sleep and irregular schedules risk](https://www.nasa.gov/reference/risk-from-inadequate-sleep-and-irregular-schedules/): sleep/circadian research context; no individual clinical threshold derived.
- [NASA CIPHER research](https://www.nasa.gov/humans-in-space/experiments-to-unlock-how-human-bodies-react-to-long-space-journeys/): multi-system/cardiovascular research context; not a diagnosis from a single bpm value.
- [NASA Astronaut Exercise](https://www.nasa.gov/missions/station/iss-research/astronaut-exercise/): exercise countermeasure context; recorded minutes do not establish muscle/bone health.

These links are visible in the deterministic explanation cards. Scientific status remains
**CORRECTIONS REQUIRED**; a scientific reviewer must assess the technical corrections separately.

## Sprint 4 follow-up — not started

1. Obtain direct official Resources/organizer confirmation of the selected resource's eligibility.
2. Obtain written scientific review of the correction matrix and the research explorer.
3. Run final offline demo QA using the documented acquisition procedure; include an honest missing-file path.
4. Review citations/license notices and the exact Git file list; keep local participant files and health entries out.
5. Prioritize final demo/presentation/submission work after Sprint 3 review. No Sprint 4 implementation occurred here.
