import pandas as pd
import pytest
import subprocess
import sys

from astrocare.analysis import analyze_daily
from astrocare.charts import trend_chart
from astrocare.data import generate_demo_data, prepare_daily_data
from astrocare.storage import StorageError, load_records, save_record


def test_empty_read_has_no_filesystem_side_effect(isolated_database):
    assert load_records().empty
    assert not isolated_database.exists()


def test_roundtrip_and_new_record_reaches_analysis_and_chart(record_factory):
    original_demo = generate_demo_data()
    save_record(record_factory(sleep_minutes=None, activity_minutes=0))
    # Independent connections simulate app restarts.
    first = load_records()
    second = load_records()
    pd.testing.assert_frame_equal(first, second)
    assert first.iloc[0].source_type == "manual_demo"
    assert bool(first.iloc[0].is_synthetic)
    assert first.iloc[0].sleep_minutes is None
    assert first.iloc[0].activity_minutes == 0
    save_record(record_factory("2026-11-16", activity_minutes=45))
    daily, _ = prepare_daily_data(load_records())
    result = analyze_daily(daily)
    assert len(result) == 2
    assert result.iloc[-1].activity_minutes_delta == 45
    assert result.iloc[-1].activity_minutes_mean7 == 22.5
    fig = trend_chart(result, "activity_minutes")
    assert list(fig.data[0].y) == [0, 45]
    pd.testing.assert_frame_equal(original_demo, generate_demo_data())


def test_duplicate_never_overwrites_existing_record(record_factory):
    save_record(record_factory())
    with pytest.raises(StorageError, match="already exists"):
        save_record(record_factory(sleep_minutes=123))
    assert len(load_records()) == 1
    assert load_records().iloc[0].sleep_minutes == 450


def test_record_is_readable_by_a_new_python_process(record_factory):
    save_record(record_factory(activity_minutes=0))
    output = subprocess.check_output([
        sys.executable, "-B", "-c",
        "from astrocare.storage import load_records; r=load_records(); "
        "assert len(r)==1; assert r.iloc[0].activity_minutes==0; print('persisted')",
    ], text=True)
    assert output.strip() == "persisted"


def test_invalid_record_does_not_create_database(record_factory, isolated_database):
    with pytest.raises(StorageError):
        save_record(record_factory(resting_hr_bpm=0))
    assert not isolated_database.exists()


def test_corrupt_database_is_not_overwritten(record_factory, isolated_database):
    isolated_database.write_bytes(b"invalid sqlite data")
    with pytest.raises(StorageError, match="could not be read"):
        load_records()
    with pytest.raises(StorageError):
        save_record(record_factory())
    assert isolated_database.read_bytes() == b"invalid sqlite data"


def test_write_error_is_readable(tmp_path, record_factory):
    blocker = tmp_path / "parent-is-file"
    blocker.write_text("keep", encoding="utf-8")
    with pytest.raises(StorageError, match="could not be saved"):
        save_record(record_factory(), blocker / "records.sqlite3")
    assert blocker.read_text() == "keep"


def test_extreme_date_span_is_rejected(record_factory):
    save_record(record_factory("2000-01-01"))
    with pytest.raises(StorageError, match="3660"):
        save_record(record_factory("2100-01-01"))
    assert len(load_records()) == 1
