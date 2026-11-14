from pathlib import Path

from streamlit.testing.v1 import AppTest

from astrocare.storage import load_records

APP = Path(__file__).resolve().parents[1] / "app.py"


def fill(app, sleep="450", hr="70", activity="0"):
    app.text_input(key="sleep_input").input(sleep)
    app.text_input(key="hr_input").input(hr)
    app.text_input(key="activity_input").input(activity)
    app.checkbox(key="rest_confirmed").check()
    return app.button[0].click().run(timeout=30)


def test_form_save_updates_cards_table_charts_and_survives_new_session():
    app = AppTest.from_file(APP).run(timeout=30)
    fill(app)
    assert not app.exception
    assert app.success
    assert app.selectbox(key="dataset").value == "Manual demo"
    assert app.metric[0].value == "7 h 30 min"
    assert len(app.get("plotly_chart")) == 3
    assert len(app.dataframe[0].value) == 1
    assert app.dataframe[0].value.iloc[0].activity_minutes == 0
    fresh = AppTest.from_file(APP).run(timeout=30)
    fresh.selectbox(key="dataset").select("Manual demo").run(timeout=30)
    assert not fresh.exception
    assert fresh.metric[0].value == "7 h 30 min"
    assert len(fresh.dataframe[0].value) == 1
    fresh.selectbox(key="dataset").select("Generated demo").run(timeout=30)
    assert len(fresh.dataframe[0].value) == 21


def test_invalid_form_does_not_save(isolated_database):
    app = AppTest.from_file(APP).run(timeout=30)
    fill(app, sleep="-1", hr="abc", activity="1441")
    assert not app.exception
    for label in ("Sleep", "Resting heart rate", "Activity"):
        assert any(label in error.value for error in app.error)
    assert not isolated_database.exists()


def test_duplicate_form_record_is_rejected():
    app = AppTest.from_file(APP).run(timeout=30)
    fill(app)
    fill(app, sleep="123")
    assert not app.exception
    assert any("already exists" in error.value for error in app.error)
    assert len(load_records()) == 1
    assert load_records().iloc[0].sleep_minutes == 450


def test_missing_field_and_zero_display_separately():
    app = AppTest.from_file(APP).run(timeout=30)
    fill(app, sleep="", activity="0")
    assert not app.exception
    assert app.metric[0].value == "No data"
    assert app.metric[2].value == "0.0 min"
    assert any("missing" in warning.value for warning in app.warning)


def test_corrupt_storage_error_does_not_crash_demo(isolated_database):
    isolated_database.write_bytes(b"invalid database")
    app = AppTest.from_file(APP).run(timeout=30)
    assert not app.exception
    assert any("could not be read" in error.value for error in app.error)
    assert len(app.get("plotly_chart")) == 3
    assert isolated_database.read_bytes() == b"invalid database"


def test_empty_manual_source_and_all_blank_form_are_safe(isolated_database):
    app = AppTest.from_file(APP).run(timeout=30)
    app.selectbox(key="dataset").select("Manual demo").run(timeout=30)
    assert not app.exception
    assert not app.metric
    fill(app, "", "", "")
    assert not app.exception
    assert app.error
    assert not isolated_database.exists()
