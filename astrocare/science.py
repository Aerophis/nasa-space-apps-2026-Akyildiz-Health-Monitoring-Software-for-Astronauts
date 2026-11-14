"""Deterministic source-backed context, separated from observed/calculated data."""

import pandas as pd

from astrocare.data import METRICS

SCIENCE_SOURCES = {
    "sleep_minutes": {
        "title": "NASA: Risk from Inadequate Sleep and Irregular Schedules",
        "url": "https://www.nasa.gov/reference/risk-from-inadequate-sleep-and-irregular-schedules/",
        "finding": "NASA studies sleep loss and circadian misalignment as concerns for human performance during spaceflight.",
        "limitation": "Duration alone does not measure sleep quality, circadian alignment, or a sleep disorder. No astronaut clinical alarm threshold is derived here.",
    },
    "resting_hr_bpm": {
        "title": "NASA: Experiments to Unlock How Human Bodies React to Long Space Journeys",
        "url": "https://www.nasa.gov/humans-in-space/experiments-to-unlock-how-human-bodies-react-to-long-space-journeys/",
        "finding": "NASA's CIPHER research examines multiple aspects of human adaptation, including cardiovascular function.",
        "limitation": "One heart rate value is not a cardiovascular assessment. Resting conditions are only declared for the fictional scenario; device calibration, posture, time of day, and signal quality are not verified.",
    },
    "activity_minutes": {
        "title": "NASA: Astronaut Exercise",
        "url": "https://www.nasa.gov/missions/station/iss-research/astronaut-exercise/",
        "finding": "NASA describes exercise as a countermeasure to the effects of spaceflight on physical conditioning.",
        "limitation": "Recorded minutes do not measure muscle mass, bone density, exercise intensity, or individual treatment needs. Exercise type and planned sessions are not tracked here.",
    },
}


def explanation_cards(daily, endpoint, comparisons):
    """Return explicit evidence categories, never generated citations or diagnoses."""
    if (daily.empty or not daily.is_synthetic.eq(True).all()
            or not daily.source_type.isin(["synthetic_demo", "manual_demo"]).all()
            or daily.source_type.nunique() != 1 or daily.subject_id.nunique() != 1):
        raise ValueError("Health explanation cards accept one synthetic demo profile/source only.")
    row = daily.loc[pd.Timestamp(endpoint)]
    by_metric = {item["metric"]: item for item in comparisons}
    cards = []
    for metric in METRICS:
        value = row[metric]
        unit = "bpm" if metric == "resting_hr_bpm" else "minutes"
        if row.get(f"{metric}_status") == "invalid":
            observed = "Invalid measurement excluded; not counted as zero."
        else:
            observed = "Missing measurement; not counted as zero." if pd.isna(value) else f"{value:g} {unit} (fictional)."
        comparison = by_metric[metric]
        cards.append({"metric": metric, "observed": observed,
                      "calculated": comparison["message"], "coverage": comparison["coverage"],
                      "design_rule": "Non-overlapping 7-day windows; at least 5 comparable observations in each. This is a prototype design rule, not a clinical threshold.",
                      "evidence_type": "Scientific background information — NASA research context",
                      **SCIENCE_SOURCES[metric]})
    return cards
