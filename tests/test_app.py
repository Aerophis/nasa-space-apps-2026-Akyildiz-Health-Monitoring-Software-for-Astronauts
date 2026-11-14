from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_dashboard_renders_and_date_controls_update():
    app = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py").run(timeout=30)
    assert not app.exception
    assert any("DEMO — SIMULATED DATA" in w.value for w in app.warning)
    assert len(app.metric) == 3
    assert len(app.get("plotly_chart")) == 3
    assert len(app.dataframe[0].value) == 21
    app.sidebar.selectbox[0].select_index(0).run(timeout=30)
    assert not app.exception
    assert len(app.dataframe[0].value) == 1
    assert all(metric.delta == "" for metric in app.metric)
    app.sidebar.selectbox[0].select_index(20)
    app.sidebar.radio[0].set_value(7).run(timeout=30)
    assert not app.exception
    assert len(app.dataframe[0].value) == 7
