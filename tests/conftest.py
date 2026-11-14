"""Never let UI tests touch a person's local record database."""

import pytest

from astrocare.data import manual_form_record


@pytest.fixture(autouse=True)
def isolated_database(tmp_path, monkeypatch):
    path = tmp_path / "records.sqlite3"
    monkeypatch.setenv("ASTROCARE_DB_PATH", str(path))
    return path


@pytest.fixture(autouse=True)
def isolated_research_directory(tmp_path, monkeypatch):
    path = tmp_path / "research"
    monkeypatch.setenv("ASTROCARE_RESEARCH_DIR", str(path))
    return path


@pytest.fixture
def record_factory():
    def make(day="2026-11-15", **changes):
        record = manual_form_record(day, "450", "70", "90", True)
        record.update(changes)
        return record
    return make
