"""Language and visibility changes must never change source data or validation."""

from pathlib import Path
from string import Formatter

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from astrocare.analysis import analyze_daily, compare_periods
from astrocare.data import generate_demo_data, prepare_daily_data, validate_health_record
from astrocare.i18n import LANGUAGES, TEXT, Translator
from astrocare.science import explanation_cards
from astrocare.ui import choice_key

APP = Path(__file__).resolve().parents[1] / "app.py"


@pytest.mark.parametrize("language", LANGUAGES)
def test_catalogue_has_all_languages_and_matching_placeholders(language):
    index = tuple(LANGUAGES).index(language)
    fields = lambda text: {(name, spec) for _, name, spec, _ in Formatter().parse(text) if name is not None}
    for key, row in TEXT.items():
        assert len(row) == len(LANGUAGES), key
        assert row[index].strip(), key
        assert fields(row[index]) == fields(row[0]), key


@pytest.mark.parametrize("language", LANGUAGES)
def test_health_language_preserves_data_and_chart_choices(language):
    app = AppTest.from_file(APP).run(timeout=30)
    original = app.dataframe[0].value.copy(deep=True)
    app.multiselect(key="visible_metrics").set_value(["sleep_minutes", "activity_minutes"]).run(timeout=30)
    app.selectbox(key="language").select(language).run(timeout=30)
    t = Translator(language)
    assert not app.exception
    assert app.warning[0].value == t("demo_warning")
    assert app.metric[0].label == t("sleep")
    assert app.selectbox(key="language").value == language
    assert len(app.get("plotly_chart")) == 2
    assert app.multiselect(key=choice_key("visible_metrics", language)).value == ["sleep_minutes", "activity_minutes"]
    assert app.multiselect(key=choice_key("visible_metrics", language)).options == [t("sleep"), t("heart"), t("activity")]
    assert len(app.get("progress")) == 3
    assert any(t("coverage_note") == c.value for c in app.caption)
    pd.testing.assert_frame_equal(app.dataframe[0].value, original)
    assert any("CORRECTIONS REQUIRED" in c.value for c in app.caption)


@pytest.mark.parametrize("selection", [
    [], ["sleep_minutes"], ["resting_hr_bpm"], ["activity_minutes"],
    ["sleep_minutes", "resting_hr_bpm"], ["sleep_minutes", "activity_minutes"],
    ["resting_hr_bpm", "activity_minutes"],
    ["sleep_minutes", "resting_hr_bpm", "activity_minutes"],
])
def test_any_chart_subset_leaves_records_and_summaries_intact(selection):
    app = AppTest.from_file(APP).run(timeout=30)
    app.multiselect(key="visible_metrics").set_value(selection).run(timeout=30)
    assert not app.exception
    assert len(app.get("plotly_chart")) == len(selection)
    assert len(app.metric) == 3
    assert len(app.dataframe[0].value) == 21
    if not selection:
        assert any(Translator()("no_charts") == info.value for info in app.info)


@pytest.mark.parametrize("language", LANGUAGES)
def test_invalid_manual_form_is_localized_and_does_not_write(language, isolated_database):
    app = AppTest.from_file(APP).run(timeout=30)
    app.selectbox(key="language").select(language).run(timeout=30)
    app.text_input(key="sleep_input").input("-1")
    app.text_input(key="hr_input").input("abc")
    app.text_input(key="activity_input").input("1441")
    app.button[0].click().run(timeout=30)
    t = Translator(language)
    assert not app.exception
    assert [error.value for error in app.error] == [
        t("invalid_duration", metric=t("sleep_short")),
        t("invalid_hr", metric=t("heart")),
        t("invalid_duration", metric=t("activity_short")),
        t("valid_required"),
    ]
    assert not isolated_database.exists()


@pytest.mark.parametrize("language", LANGUAGES)
def test_science_and_domain_messages_have_no_unknown_fallback(language, record_factory):
    daily = prepare_daily_data(generate_demo_data())[0]
    endpoint = daily.index[-1]
    comparisons = compare_periods(daily, endpoint)
    messages = []
    for card in explanation_cards(daily, endpoint, comparisons):
        messages.extend(card[k] for k in ("observed", "calculated", "coverage", "design_rule", "finding", "limitation"))
    for comparison in compare_periods(daily.iloc[:2], daily.index[1]):
        messages.extend([comparison["message"], comparison["coverage"]])
    invalid = record_factory(sleep_minutes=-1, activity_minutes=None)
    result = validate_health_record(invalid)
    messages.extend(result.errors + result.warnings)
    t = Translator(language)
    for message in messages:
        translated = t.message(message)
        assert t("technical_detail", detail=message) != translated
    assert analyze_daily(daily).sleep_minutes.equals(daily.sleep_minutes)


@pytest.mark.parametrize("language", LANGUAGES)
def test_missing_research_has_localized_error_and_findable_provenance(language):
    app = AppTest.from_file(APP).run(timeout=30)
    app.selectbox(key="language").select(language).run(timeout=30)
    app.radio(key=choice_key("workspace", language)).set_value("NASA Research Data Explorer").run(timeout=30)
    t = Translator(language)
    assert not app.exception
    assert app.error[0].value == t("missing_research")
    assert not app.get("plotly_chart")
    header = next(item.value for item in app.markdown if 'data-testid="research-header"' in item.value)
    assert 'data-testid="research-verified"' not in header
    details = next(exp for exp in app.expander if exp.label == t("provenance"))
    assert any("CC0-1.0" in item.value and "osdr.nasa.gov" in item.value for item in details.markdown)
    assert any("CORRECTIONS REQUIRED" in caption.value for caption in app.caption)


def test_unknown_diagnostic_is_explicit_and_unsupported_language_is_rejected():
    assert Translator("tr").message("Unexpected diagnostic") == Translator("tr")("technical_detail", detail="Unexpected diagnostic")
    with pytest.raises(ValueError):
        Translator("xx")


def test_locale_round_trip_preserves_date_range_and_selected_charts():
    app = AppTest.from_file(APP).run(timeout=30)
    app.sidebar.selectbox[0].select_index(15).run(timeout=30)
    selected_date = app.sidebar.selectbox[0].value
    app.radio(key="chart_range").set_value(7).run(timeout=30)
    app.multiselect(key="visible_metrics").set_value(["activity_minutes"]).run(timeout=30)
    original = app.dataframe[0].value.copy(deep=True)
    for language in ["tr", "de", "en"]:
        app.selectbox(key="language").select(language).run(timeout=30)
        assert not app.exception
        assert app.sidebar.selectbox[0].value == selected_date
        assert app.radio(key=choice_key("chart_range", language)).value == 7
        assert app.multiselect(key=choice_key("visible_metrics", language)).value == ["activity_minutes"]
        pd.testing.assert_frame_equal(app.dataframe[0].value, original)


def test_locale_round_trip_and_save_preserve_manual_source(record_factory):
    from astrocare.storage import save_record

    save_record(record_factory())
    app = AppTest.from_file(APP).run(timeout=30)
    app.selectbox(key="dataset").select("Manual demo").run(timeout=30)
    original = app.dataframe[0].value.copy(deep=True)
    for language in ["es", "fr", "en"]:
        app.selectbox(key="language").select(language).run(timeout=30)
        assert not app.exception
        assert app.selectbox(key=choice_key("dataset", language)).value == "Manual demo"
        pd.testing.assert_frame_equal(app.dataframe[0].value, original)


@pytest.mark.parametrize("language", LANGUAGES)
def test_localized_save_selects_manual_source_and_keeps_missing_distinct_from_zero(language):
    from astrocare.storage import load_records

    app = AppTest.from_file(APP).run(timeout=30)
    app.selectbox(key="language").select(language).run(timeout=30)
    app.text_input(key="sleep_input").input("")
    app.text_input(key="hr_input").input("70")
    app.text_input(key="activity_input").input("0")
    app.checkbox(key="rest_confirmed").check()
    app.button[0].click().run(timeout=30)
    t = Translator(language)
    assert not app.exception
    assert app.success[0].value == t("saved")
    assert app.selectbox(key=choice_key("dataset", language)).value == "Manual demo"
    assert app.metric[0].value == t("no_data")
    assert app.metric[2].value == "0.0 " + t("min")
    assert any(w.value == t("missing_metric", metric=t("sleep_short")) for w in app.warning)
    saved = load_records()
    assert len(saved) == 1
    assert pd.isna(saved.iloc[0].sleep_minutes)
    assert saved.iloc[0].activity_minutes == 0
    assert saved.source_type.eq("manual_demo").all()
    assert saved.is_synthetic.eq(True).all()
