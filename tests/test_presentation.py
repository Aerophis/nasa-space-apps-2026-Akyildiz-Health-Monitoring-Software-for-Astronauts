"""Presentation changes must retain measurement semantics and data gaps."""

import numpy as np
import pytest

from astrocare.analysis import analyze_daily
from astrocare.charts import trend_chart
from astrocare.data import generate_demo_data, prepare_daily_data


@pytest.mark.parametrize("metric,kind,fill", [
    ("sleep_minutes", "scatter", "tozeroy"),
    ("resting_hr_bpm", "scatter", None),
    ("activity_minutes", "bar", None),
])
def test_distinct_health_styles_preserve_missing_days_and_source(metric, kind, fill):
    daily = analyze_daily(prepare_daily_data(generate_demo_data().drop(index=10))[0])
    fig = trend_chart(daily, metric)
    assert fig.data[0].type == kind
    if kind == "scatter":
        assert fig.data[0].fill == fill
        assert fig.data[0].connectgaps is False
    np.testing.assert_allclose(fig.data[0].y, daily[metric], equal_nan=True)
    assert np.isnan(fig.data[0].y[10])
    assert fig.data[1].connectgaps is False
    assert "DEMO — SIMULATED DATA" in fig.layout.annotations[0].text
    assert "synthetic_demo" in fig.layout.annotations[0].text
    assert fig.layout.yaxis.rangemode == (None if metric == "resting_hr_bpm" else "tozero")
