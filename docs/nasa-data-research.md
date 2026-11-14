# NASA data research — Sprint 2

Review date: 14 November 2026. Real NASA data have not been integrated into the application.

## Access and evidence

| Source | Check performed during the implementation session | Decision |
| --- | --- | --- |
| [Official challenge Resources](https://www.spaceappschallenge.org/2026/challenges/health-monitoring-software/?tab=resources) | The direct request failed with a tool access error. The main challenge URL also returned 502. The challenge title was found in the search index. | A search listing does not verify the complete Resources list. The list and source suitability remain unresolved. |
| [OSDR OSD-575](https://osdr.nasa.gov/bio/repo/data/studies/OSD-575) | The NASA search record identifies Inspiration4 serum metabolic panels and immune/cardiac cytokine arrays, version 3. The opened dynamic page returned no readable lines. | Not used as a daily series for the three metrics. No data file was downloaded or processed. |
| [NASA I4 Mission Datasets](https://www.nasa.gov/osdr-latest-news-i4-mission-datasets/) | The official NASA search record lists OSD-575 as Blood Serum. | Context for the data type, not evidence of a sleep/heart-rate/exercise series or application integration. |

The local scientific documents also describe OSD-575 as unsuitable for direct
mapping to the first three metrics. Their CC0 statement was not reverified at
file level in this session; no third-party file was redistributed on that assumption.
The scientific PDF/DOCX files were not modified and are not included in delivery.

## Sprint 3 research/integration task — not started

1. Verify the official Resources list through the website or organizers. Record the
   specific NASA source URL, access date, and relationship to the challenge.
2. Identify an actual downloadable file and verify its measurement type,
   human/analog/environmental classification, schema, units, and file-level license/access conditions.
3. If a suitable source exists, design a separate real-data profile/source layer;
   download a sample and test the transformation and provenance. Do not combine it with synthetic data.
4. If no directly matching series is available, clarify acceptable NASA source use
   with the organizers. Do not relabel serum chemistry as sleep/bpm/exercise.
5. Acceptance evidence: source URL, file/version, license, field mapping, and an
   actual download/processing test. Do not state "NASA data integrated" without this evidence.

Core Sprint 2 development proceeded independently of this access blocker using
fictional demo data only. Scientific acceptance and challenge source suitability remain open.
