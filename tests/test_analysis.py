import numpy as np
import pandas as pd
import pytest

from astrocare.analysis import analyze_daily
from astrocare.charts import trend_chart
from astrocare.data import METRICS, REQUIRED, generate_demo_data, prepare_daily_data


def test_demo_reproducible_and_explicitly_synthetic():
    raw = generate_demo_data()
    pd.testing.assert_frame_equal(raw, generate_demo_data())
    assert len(raw) >= 14
    assert set(REQUIRED) == set(raw.columns)
    assert raw.is_synthetic.all()
    assert raw.source_type.eq("synthetic_demo").all()
    assert raw.subject_id.nunique() == 1
    daily, notices = prepare_daily_data(raw)
    assert not notices
    assert daily[list(METRICS)].notna().all().all()


def test_calendar_gaps_do_not_compare_with_last_observation():
    raw = generate_demo_data().drop(index=1)
    daily, notices = prepare_daily_data(raw)
    result = analyze_daily(daily)
    assert notices
    assert result.iloc[1][list(METRICS)].isna().all()
    for metric in METRICS:
        assert pd.isna(result.iloc[2][f"{metric}_delta"])
        assert result.iloc[2][f"{metric}_count7"] == 2
        assert result.iloc[2][f"{metric}_mean7"] == pytest.approx(daily[metric].iloc[:3].mean())


def test_rolling_window_and_daily_delta():
    raw = generate_demo_data()
    raw["activity_minutes"] = list(range(21))
    result = analyze_daily(prepare_daily_data(raw)[0])
    assert result.iloc[0].activity_minutes_count7 == 1
    assert pd.isna(result.iloc[0].activity_minutes_delta)
    assert result.iloc[6].activity_minutes_mean7 == 3
    assert result.iloc[7].activity_minutes_mean7 == 4
    assert result.iloc[-1].activity_minutes_delta == 1
    assert result.iloc[-1].activity_minutes_count7 == 7


@pytest.mark.parametrize("metric,value", [
    ("sleep_minutes", -1), ("sleep_minutes", 1441),
    ("resting_hr_bpm", 0), ("resting_hr_bpm", float("inf")),
    ("activity_minutes", "bad"), ("activity_minutes", None),
])
def test_invalid_cells_become_missing(metric, value):
    raw = generate_demo_data().astype({metric: object})
    raw.loc[0, metric] = value
    daily, notices = prepare_daily_data(raw)
    assert pd.isna(daily.iloc[0][metric])
    assert notices


def test_all_missing_metric_has_no_average():
    raw = generate_demo_data()
    raw["sleep_minutes"] = None
    result = analyze_daily(prepare_daily_data(raw)[0])
    assert result.sleep_minutes_mean7.isna().all()
    assert result.sleep_minutes_count7.eq(0).all()


def test_invalid_date_is_excluded_and_input_not_modified():
    raw = generate_demo_data().astype({"measured_at": object})
    raw.loc[2, "measured_at"] = "invalid"
    before = raw.copy(deep=True)
    daily, notices = prepare_daily_data(raw)
    pd.testing.assert_frame_equal(raw, before)
    assert len(notices) == 2
    assert daily.iloc[2][list(METRICS)].isna().all()


@pytest.mark.parametrize("kind", ["empty", "schema", "duplicate", "subject", "real", "dates"])
def test_unsafe_inputs_are_rejected(kind):
    raw = generate_demo_data()
    if kind == "empty":
        raw = raw.iloc[:0]
    elif kind == "schema":
        raw = raw.drop(columns="source_type")
    elif kind == "duplicate":
        raw = pd.concat([raw, raw.iloc[:1]])
    elif kind == "subject":
        raw.loc[0, "subject_id"] = "other"
    elif kind == "real":
        raw.loc[0, "is_synthetic"] = False
    elif kind == "dates":
        raw["measured_at"] = "invalid"
    with pytest.raises(ValueError):
        prepare_daily_data(raw)


@pytest.mark.parametrize("metric", METRICS)
def test_chart_matches_measurements_and_rolling_series(metric):
    raw = generate_demo_data().drop(index=10)
    result = analyze_daily(prepare_daily_data(raw)[0]).iloc[-14:]
    fig = trend_chart(result, metric)
    assert list(fig.data[0].x) == list(result.index.to_pydatetime())
    np.testing.assert_allclose(fig.data[0].y, result[metric], equal_nan=True)
    np.testing.assert_allclose(fig.data[1].y, result[f"{metric}_mean7"], equal_nan=True)
    assert fig.data[0].connectgaps is False
    assert fig.layout.yaxis.title.text == ("bpm" if metric == "resting_hr_bpm" else "minutes")
    assert fig.to_json()
