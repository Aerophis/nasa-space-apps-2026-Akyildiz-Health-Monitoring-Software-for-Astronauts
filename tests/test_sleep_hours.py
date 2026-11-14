import pandas as pd 
from astrocare.analysis import analyze_daily

def test_sleep_minutes_to_hours():
    data = pd.DataFrame({
        "sleep_minutes": [450],
        "resting_hr_bpm": [70],
        "activity_minutes": [90],
    })

    result = analyze_daily(data)
    assert result.loc[0, "sleep_hours"] == 7.5


def test_missing_sleep_data():
    data = pd.DataFrame({
        "sleep_minutes": [450, None],
        "resting_hr_bpm": [70, 72],
        "activity_minutes": [90,80],
    })

    result = analyze_daily(data)
    assert pd.isna(result.loc[1, "sleep_hours"])