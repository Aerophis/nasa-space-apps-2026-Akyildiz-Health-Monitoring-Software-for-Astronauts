"""Calendar-based summaries without medical thresholds or risk scores."""

import pandas as pd

from astrocare.data import METRICS


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
