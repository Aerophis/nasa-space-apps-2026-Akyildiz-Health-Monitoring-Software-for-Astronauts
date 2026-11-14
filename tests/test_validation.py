import pandas as pd
import pytest

from astrocare.data import (
    classify_activity_minutes, classify_measurement, classify_resting_hr,
    manual_form_record, prepare_daily_data, validate_health_record,
)


@pytest.mark.parametrize("value,expected", [
    (None, "missing"), (float("nan"), "missing"), (pd.NA, "missing"),
    (0, "invalid"), (-1, "invalid"), (float("inf"), "invalid"),
    (-float("inf"), "invalid"), (True, "invalid"), ("70", "invalid"),
    ([], "invalid"), ({}, "invalid"), (0.1, "valid"), (70, "valid"), (1000, "valid"),
    (10 ** 1000, "invalid"),
])
def test_resting_hr_data_format_only(value, expected):
    assert classify_resting_hr(value) == expected


@pytest.mark.parametrize("value,expected", [
    (None, "missing"), (float("nan"), "missing"), (-1, "invalid"),
    (0, "valid"), (1440, "valid"), (1440.1, "invalid"),
    (False, "invalid"), ("90", "invalid"), (float("inf"), "invalid"),
    ([], "invalid"), (0.5, "valid"),
])
def test_activity_boundaries(value, expected):
    assert classify_activity_minutes(value) == expected


@pytest.mark.parametrize("value,expected", [(450, "valid"), (-1, "invalid"), (None, "missing"),
                                         ("450", "invalid"), (True, "invalid"), ([], "invalid")])
def test_sleep_adapter_preserves_original_function(value, expected):
    assert classify_measurement(value, "sleep_minutes") == expected


@pytest.mark.parametrize("value", ["wrong", "2026-02-30", "14/11/2026", 123, None, [], "2200-01-01"])
def test_record_invalid_dates(record_factory, value):
    assert not validate_health_record(record_factory(measured_at=value)).ok


def test_missing_distinct_from_invalid_and_zero(record_factory):
    result = validate_health_record(record_factory(sleep_minutes=None, activity_minutes=0))
    assert result.ok
    assert result.record["sleep_minutes"] is None
    assert result.record["activity_minutes"] == 0
    assert result.statuses["sleep_minutes"] == "missing"
    assert result.warnings
    bad = validate_health_record(record_factory(sleep_minutes=-1))
    assert not bad.ok
    assert bad.statuses["sleep_minutes"] == "invalid"
    assert any("Sleep" in error for error in bad.errors)


@pytest.mark.parametrize("changes", [
    {"sleep_minutes_unit": "hour"}, {"resting_hr_bpm_unit": "Hz"},
    {"activity_minutes_unit": "second"}, {"sleep_minutes": True},
    {"source_type": "device"}, {"is_synthetic": False}, {"subject_id": "real-person"},
    {"rest_state": "active"},
    {"subject_id": pd.NA}, {"source_type": []}, {"rest_state": pd.NA},
    {"sleep_minutes_unit": pd.NA},
])
def test_record_rejects_units_types_and_wrong_origin(record_factory, changes):
    assert not validate_health_record(record_factory(**changes)).ok


def test_duplicate_and_all_missing_are_rejected(record_factory):
    assert not validate_health_record(record_factory(), ["2026-11-15"]).ok
    assert not validate_health_record(record_factory(sleep_minutes=None, resting_hr_bpm=None, activity_minutes=None)).ok
    assert not validate_health_record([]).ok


def test_form_parser_supports_blank_decimal_comma_and_invalid_text():
    record = manual_form_record("2026-11-15", "450,5", "", "0")
    result = validate_health_record(record)
    assert result.ok
    assert result.record["sleep_minutes"] == 450.5
    assert result.record["resting_hr_bpm"] is None
    assert result.record["activity_minutes"] == 0
    assert not validate_health_record(manual_form_record("2026-11-15", "abc", "70", "90")).ok


def test_prepare_preserves_quality_categories(record_factory):
    raw = pd.DataFrame([record_factory(sleep_minutes=None, activity_minutes=-1)])
    daily, notices = prepare_daily_data(raw)
    assert daily.iloc[0].sleep_minutes_status == "missing"
    assert daily.iloc[0].activity_minutes_status == "invalid"
    assert len(notices) == 2
    assert daily.source_type.eq("manual_demo").all()
