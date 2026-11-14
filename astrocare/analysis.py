"""Calendar-based summaries without medical thresholds or risk scores."""

import pandas as pd

from astrocare.data import METRICS, LABELS


def analyze_daily(daily: pd.DataFrame) -> pd.DataFrame:
    """Input is a sorted, complete daily calendar from prepare_daily_data."""
    result = daily.copy()
    
    result["sleep_hours"] = result["sleep_minutes"] / 60
    
    for metric in METRICS:
        values = result[metric]
        result[f"{metric}_delta"] = values.diff()
        result[f"{metric}_mean7"] = values.rolling(7, min_periods=1).mean()
        result[f"{metric}_count7"] = values.rolling(7, min_periods=1).count().astype(int)
    return result


def compare_periods(daily, endpoint, min_valid=5):
    """Two disjoint calendar weeks, same fictional subject/source.

    Five comparable observations per week is a transparent demo design choice,
    not a clinically validated minimum. Unknown rest conditions are excluded
    from the resting-HR comparison, never interpreted as a medical event.
    """
    if not 1 <= min_valid <= 7:
        raise ValueError("The minimum observation count for comparisons must be between 1 and 7.")
    if daily.subject_id.nunique() != 1 or daily.source_type.nunique() != 1:
        raise ValueError("Different subjects or data sources cannot be compared.")
    end = pd.Timestamp(endpoint).normalize()
    rows = []
    for metric in METRICS:
        values = daily[metric]
        if metric == "resting_hr_bpm":
            if "rest_state" not in daily:
                values = values.where(daily.source_type.eq("synthetic_demo"))
            else:
                values = values.where(daily.rest_state.isin(["confirmed", "simulated_rest"]))
        baseline = values.loc[end - pd.Timedelta(days=13):end - pd.Timedelta(days=7)].dropna()
        current = values.loc[end - pd.Timedelta(days=6):end].dropna()
        enough = len(baseline) >= min_valid and len(current) >= min_valid
        delta = float(current.mean() - baseline.mean()) if enough else None
        unit = "bpm" if metric == "resting_hr_bpm" else "minutes"
        coverage = f"Baseline: {len(baseline)}/7; comparison: {len(current)}/7 comparable records."
        if enough:
            message = f"The {LABELS[metric]} average changed by {delta:+.1f} {unit} compared with the separate preceding week. This difference alone does not establish a medical finding."
        else:
            message = f"Insufficient data for {LABELS[metric]}; no trend interpretation is shown. At least {min_valid} comparable records are required in each period."
        rows.append({"metric": metric, "baseline_count": len(baseline), "current_count": len(current),
                     "baseline_mean": float(baseline.mean()) if len(baseline) else None,
                     "current_mean": float(current.mean()) if len(current) else None,
                     "delta": delta, "enough": enough, "message": message, "coverage": coverage})
    return rows
