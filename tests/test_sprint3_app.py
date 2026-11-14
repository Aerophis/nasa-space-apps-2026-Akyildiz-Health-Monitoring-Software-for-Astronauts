from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def test_missing_dataset_workspace_is_honest_and_health_dashboard_survives():
    app = AppTest.from_file(APP).run(timeout=30)
    assert not app.exception
    assert any("SIMULATED HEALTH TELEMETRY" in c.value for c in app.caption)
    app.radio(key="workspace").set_value("NASA Research Data Explorer").run(timeout=30)
    assert not app.exception
    assert app.error
    assert not app.success
    assert not app.get("plotly_chart")
    assert any("numerical research integration is unavailable" in i.value for i in app.info)
    app.radio(key="workspace").set_value("Health dashboard").run(timeout=30)
    assert not app.exception
    assert len(app.metric) == 3
    assert len(app.get("plotly_chart")) == 3


def test_unconfirmed_manual_resting_conditions_suppress_daily_delta(record_factory):
    from astrocare.storage import save_record

    save_record(record_factory("2026-11-14", rest_state="unspecified"))
    save_record(record_factory("2026-11-15", resting_hr_bpm=80, rest_state="confirmed"))
    app = AppTest.from_file(APP).run(timeout=30)
    app.selectbox(key="dataset").select("Manual demo").run(timeout=30)
    assert not app.exception
    assert app.metric[1].delta == ""
    assert any("MANUALLY ENTERED DEMO DATA" in c.value for c in app.caption)
