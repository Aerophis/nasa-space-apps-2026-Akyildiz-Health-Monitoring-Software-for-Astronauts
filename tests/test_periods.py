import pandas as pd
import pytest

from astrocare.analysis import compare_periods
from astrocare.data import generate_demo_data, prepare_daily_data
from astrocare.charts import trend_chart


def test_disjoint_baseline_and_comparison_windows():
    raw = generate_demo_data()
    raw["sleep_minutes"] = [300] * 14 + [420] * 7
    daily, _ = prepare_daily_data(raw)
    row = compare_periods(daily, daily.index[-1])[0]
    assert row["baseline_count"] == row["current_count"] == 7
    assert row["baseline_mean"] == 300
    assert row["current_mean"] == 420
    assert row["delta"] == 120


def test_low_coverage_suppresses_interpretation():
    daily, _ = prepare_daily_data(generate_demo_data().iloc[:3])
    for row in compare_periods(daily, daily.index[-1]):
        assert not row["enough"]
        assert row["delta"] is None
        assert "Insufficient data" in row["message"]


def test_unconfirmed_resting_conditions_not_compared():
    daily, _ = prepare_daily_data(generate_demo_data())
    daily["source_type"] = "manual_demo"
    daily["rest_state"] = "unspecified"
    hr = compare_periods(daily, daily.index[-1])[1]
    assert hr["baseline_count"] == hr["current_count"] == 0
    assert hr["delta"] is None
    daily["rest_state"] = "confirmed"
    assert compare_periods(daily, daily.index[-1])[1]["enough"]


def test_missing_records_are_not_included_as_zero():
    raw = generate_demo_data()
    raw["activity_minutes"] = 90.0
    raw.loc[20, "activity_minutes"] = float("nan")
    daily, _ = prepare_daily_data(raw)
    result = compare_periods(daily, daily.index[-1])[2]
    assert result["current_count"] == 6
    assert result["current_mean"] == 90
    assert result["delta"] == 0


def test_mixed_sources_and_subjects_rejected():
    daily, _ = prepare_daily_data(generate_demo_data())
    daily.loc[daily.index[-1], "subject_id"] = "another"
    with pytest.raises(ValueError):
        compare_periods(daily, daily.index[-1])


def test_exportable_chart_keeps_demo_origin_label():
    from astrocare.analysis import analyze_daily

    daily, _ = prepare_daily_data(generate_demo_data())
    fig = trend_chart(analyze_daily(daily), "sleep_minutes")
    assert "DEMO — SIMULATED DATA" in fig.layout.annotations[0].text
    assert "synthetic_demo" in fig.layout.annotations[0].text
